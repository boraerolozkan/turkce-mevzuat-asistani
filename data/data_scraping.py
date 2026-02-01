import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Dosyaların kaydedileceği yer (Proje yapısına uygun )
DOWNLOAD_DIR = "mevzuat"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def download_file(url, filename):
    """Verilen URL'deki dosyayı indirir."""
    try:
        # Dosya ismindeki geçersiz karakterleri temizle
        safe_filename = "".join([c if c.isalnum() or c in " .-_" else "_" for c in filename])
        # Uzantı kontrolü
        if not safe_filename.endswith(".pdf"):
            safe_filename += ".pdf"
            
        path = os.path.join(DOWNLOAD_DIR, safe_filename)
        
        # User-Agent ekleyerek bot gibi görünmeyi engellemeye çalışalım
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, stream=True)
        
        if response.status_code == 200:
            with open(path, 'wb') as f:
                f.write(response.content)
            print(f"✅ İNDİRİLDİ: {safe_filename}")
        else:
            print(f"❌ İNDİRİLEMEDİ ({response.status_code}): {url}")
    except Exception as e:
        print(f"❌ HATA: {e}")

def scrape_mevzuat(driver, category_url, category_name, limit=10):
    print(f"\n--- {category_name} Taranıyor ---")
    driver.get(category_url)
    
    wait = WebDriverWait(driver, 20)
    
    # URL'den tab ID'sini çek (örn: #kanunlar -> kanunlar)
    tab_id = category_url.split("#")[-1] if "#" in category_url else None

    try:
        # 1. 'Ara' butonuna bas
        if tab_id:
            # Sadece ilgili tab altındaki butonu bul
            xpath = f"//*[@id='{tab_id}']//button[contains(text(), 'Ara')]"
        else:
            xpath = "//button[contains(text(), 'Ara')]"
            
        print(f"🔍 Buton aranıyor: {xpath}")
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        
        # Olası overlay veya görünürlük sorunları için scroll
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_btn)
        time.sleep(0.5)
        search_btn.click()
        print("🔍 'Ara' butonuna basıldı, sonuçlar bekleniyor...")
        
        # 2. Yükleniyor animasyonunun kaybolmasını bekle
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "loaderContainer")))
        except:
            pass
        wait.until(EC.invisibility_of_element_located((By.ID, "loaderContainer")))
        
        # Tablonun görünür olduğundan da emin ol
        wait.until(lambda d: "d-none" not in d.find_element(By.ID, "searchTable").get_attribute("class"))
        print("📄 Tablo yüklendi.")
        
        # Sayfa başına kayıt sayısını 100 yap (Pagination sayısını azaltmak için)
        try:
            length_select = Select(driver.find_element(By.CSS_SELECTOR, "select[name$='_length']"))
            length_select.select_by_value("100")
            print("� Sayfa başı kayıt sayısı 100'e çıkarıldı.")
            # Seçimden sonra tablonun güncellenmesini bekle
            try:
                WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "loaderContainer")))
            except:
                pass
            wait.until(EC.invisibility_of_element_located((By.ID, "loaderContainer")))
        except Exception as e:
            print(f"⚠️ Sayfa limiti değiştirilemedi: {e}")

        # 3. Pagination Dögüsü
        all_row_data = []
        
        while True:
            # Mevcut sayfadaki satırları al
            rows = driver.find_elements(By.CSS_SELECTOR, "#searchTable table tbody tr")
            
            for row in rows:
                if limit and len(all_row_data) >= limit:
                    break
                    
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) < 3: continue
                
                mevzuat_no = cols[0].text.strip()
                mevzuat_adi = cols[1].text.strip()
                
                try:
                    link_elem = row.find_element(By.TAG_NAME, "a")
                    href = link_elem.get_attribute("href")
                    all_row_data.append({
                        "no": mevzuat_no,
                        "adi": mevzuat_adi,
                        "href": href
                    })
                except:
                    continue
            
            if limit and len(all_row_data) >= limit:
                print(f"🛑 Limit ({limit}) hedefine ulaşıldı.")
                break
                
            # Sonraki Sayfaya Geçiş Kontrolü
            # Mantık: Aktif sayfa numarasını bul, bir sonrakini (current + 1) ara ve tıkla.
            try:
                pagination_ul = driver.find_element(By.CSS_SELECTOR, ".dataTables_paginate .pagination")
                active_li = pagination_ul.find_element(By.CSS_SELECTOR, "li.active")
                current_page_num = int(active_li.text)
                target_page_num = current_page_num + 1
                
                # Hedef sayfa numarasını içeren linki bul (tam eşleşme)
                # XPath: .//a[text()='6'] gibi
                next_page_link = pagination_ul.find_element(By.XPATH, f".//a[text()='{target_page_num}']")
                
                print(f"➡️ Sonraki sayfaya geçiliyor: {target_page_num}")
                next_page_link.click()
                
                # Sayfa geçişini bekle
                try:
                    WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "loaderContainer")))
                except:
                    pass
                wait.until(EC.invisibility_of_element_located((By.ID, "loaderContainer")))
                
            except NoSuchElementException:
                print("🏁 Başka sayfa kalmadı veya 'Sonraki' butonu bulunamadı.")
                break
            except Exception as e:
                print(f"⚠️ Sayfa geçişinde hata: {e}")
                break

        print(f"Toplam {len(all_row_data)} adet kayıt işlenecek.")

        # 4. Linkleri işle
        for item in all_row_data:
            full_url = item['href']
            if not full_url.startswith("http"):
                full_url = "https://www.mevzuat.gov.tr" + full_url
                
            # ... (geri kalan indirme kodu aynı)
            file_name = f"{category_name}_{item['no']}_{item['adi'][:150]}"
            
            # --- SENARYO 1: Direkt PDF (Cumhurbaşkanı Kararları vb.) ---
            if full_url.lower().endswith(".pdf"):
                print(f"⬇️ Direkt PDF indiriliyor: {item['no']} - {item['adi'][:30]}...")
                download_file(full_url, file_name)
            
            # --- SENARYO 2: Detay Sayfası (Kanunlar vb.) ---
            else:
                # print(f"🔗 Detay sayfasına gidiliyor: {item['adi']}") # Log kirliliği olmasın
                
                # Yeni sekmede açıp işi bitirip kapatmak ana listeyi korur
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                driver.get(full_url)
                
                try:
                    # PDF ikonunu/linkini bul
                    pdf_link_elem = wait.until(EC.presence_of_element_located(
                        (By.XPATH, "//a[contains(@href, '.pdf') and .//img[contains(@src, 'iconPdf')]]")
                    ))
                    pdf_url = pdf_link_elem.get_attribute("href")
                    
                    if not pdf_url.startswith("http"):
                        pdf_url = "https://www.mevzuat.gov.tr" + pdf_url
                        
                    print(f"   ⬇️ PDF bulundu: {file_name[:30]}...")
                    download_file(pdf_url, file_name)
                    
                except Exception as e:
                    print(f"   ⚠️ PDF butonu bulunamadı: {file_name}")
                
                # Sekmeyi kapat ve ana listeye dön
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(0.5)

    except Exception as e:
        print(f"Genel Hata: {e}")

def main():
    driver = setup_driver()
    try:
        # KANUNLAR (Detay sayfasına yönlendirir)
        # URL'nin sonundaki #kanunlar kısmı Selenium için sadece başlangıç noktasıdır,
        # buton tıklamaları gerekebilir.
        scrape_mevzuat(driver, "https://www.mevzuat.gov.tr/#kanunHukmundeKararnameler", "KHK", limit=63)
        
        # CUMHURBAŞKANI KARARLARI (Genellikle direkt PDF açar)
        #scrape_mevzuat(driver, "https://www.mevzuat.gov.tr/#cumhurbaskaniKararlari", "CB_Karar", limit=5)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
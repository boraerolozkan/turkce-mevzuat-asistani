import os

def count_files(directory):
    if not os.path.exists(directory):
        print(f"❌ Klasör bulunamadı: {directory}")
        return

    file_count = 0
    pdf_count = 0
    
    print(f"📂 '{directory}' klasörü taranıyor...")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_count += 1
            if file.lower().endswith('.pdf'):
                pdf_count += 1
    
    print("-" * 30)
    print(f"Toplam Dosya Sayısı: {file_count}")
    print(f"PDF Dosya Sayısı   : {pdf_count}")
    print("-" * 30)

if __name__ == "__main__":
    # Scriptin bulunduğu dizindeki 'data' klasörünü sayar
    target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mevzuat")
    count_files(target_dir)

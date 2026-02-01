#!/bin/bash
# Deployment script for boraozkan.com/turkce-mevzuat-asistani
# Sunucuda çalıştırılacak

set -e

echo "🚀 Mevzuat Asistanı Deployment Başlıyor..."

# Değişkenler
APP_DIR="/home/$USER/turkce-mevzuat-asistani"
WEB_DIR="/var/www/turkce-mevzuat-asistani"
DOMAIN="boraozkan.com"

# 1. Repo'yu güncelle
echo "📥 Repo güncelleniyor..."
cd $APP_DIR
git pull origin main

# 2. Frontend build
echo "🔨 Frontend build ediliyor..."
cd $APP_DIR/frontend
npm install
VITE_BASE_PATH=/turkce-mevzuat-asistani/ \
VITE_API_URL=https://$DOMAIN/turkce-mevzuat-asistani \
npm run build

# 3. Build dosyalarını web dizinine kopyala
echo "📁 Dosyalar kopyalanıyor..."
sudo mkdir -p $WEB_DIR
sudo cp -r dist/* $WEB_DIR/
sudo chown -R www-data:www-data $WEB_DIR

# 4. Backend'i yeniden başlat
echo "🔄 Backend yeniden başlatılıyor..."
cd $APP_DIR
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# 5. Nginx'i yeniden yükle
echo "🔄 Nginx yeniden yükleniyor..."
sudo nginx -t && sudo systemctl reload nginx

echo "✅ Deployment tamamlandı!"
echo "🌐 Site: https://$DOMAIN/turkce-mevzuat-asistani"

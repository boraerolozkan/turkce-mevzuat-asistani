# frontend/Dockerfile
FROM node:22-alpine

WORKDIR /app

# Bağımlılıkları yükle
COPY package*.json ./
RUN npm install

# Kodları kopyala
COPY . .

# Vite sunucusunu dışarıya açmak için host ayarı
EXPOSE 5173

# Başlat
CMD ["npm", "run", "dev", "--", "--host"]
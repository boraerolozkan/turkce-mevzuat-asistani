import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],

  // Production'da sub-path kullanımı için
  // boraozkan.com/turkce-mevzuat-asistani şeklinde erişim
  base: process.env.VITE_BASE_PATH || '/',

  server: {
    host: true,
    port: 5173
  },

  build: {
    outDir: 'dist',
    sourcemap: false
  }
})

import axios from 'axios';

// API Base URL - environment variable'dan veya varsayılan değerden al
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Axios instance oluştur
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60 saniye timeout (LLM cevabı zaman alabilir)
});

/**
 * Chat API'ye soru gönderir ve cevap alır
 * @param {string} question - Kullanıcının sorusu
 * @returns {Promise<{answer: string, sources: Array}>}
 */
export const sendChatMessage = async (question) => {
  try {
    const response = await apiClient.post('/api/chat', {
      question: question,
    });

    return {
      answer: response.data.answer,
      sources: response.data.sources || [],
    };
  } catch (error) {
    console.error('API Hatası:', error);

    if (error.response) {
      // Sunucu yanıt verdi ama hata kodu döndü
      throw new Error(error.response.data.detail || 'Sunucu hatası oluştu');
    } else if (error.request) {
      // İstek gönderildi ama yanıt alınamadı
      throw new Error('Sunucuya bağlanılamadı. Backend çalışıyor mu?');
    } else {
      // İstek oluşturulurken hata oluştu
      throw new Error('Bir hata oluştu: ' + error.message);
    }
  }
};

/**
 * API sağlık kontrolü
 * @returns {Promise<boolean>}
 */
export const checkHealth = async () => {
  try {
    const response = await apiClient.get('/');
    return response.data.status === 'ok';
  } catch {
    return false;
  }
};

export default apiClient;

import { useState, useCallback } from 'react';
import { sendChatMessage } from '../services/api';

/**
 * Chat state yönetimi için custom hook
 */
const useChat = () => {
  // Mesaj geçmişi
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: 'Merhaba! Ben Türk Mevzuat Asistanı. Kanunlar ve yönetmelikler hakkında bana soru sorabilirsin. Aşağıdaki örnek sorulardan birini seçebilir veya kendi sorunuzu yazabilirsiniz.',
      sources: [],
    },
  ]);

  // Yükleniyor durumu
  const [isLoading, setIsLoading] = useState(false);

  // Hata durumu
  const [error, setError] = useState(null);

  // Öneri sorularını göster/gizle
  const [showSuggestions, setShowSuggestions] = useState(true);

  /**
   * Yeni mesaj gönder
   * @param {string} question - Kullanıcının sorusu
   */
  const sendMessage = useCallback(async (question) => {
    if (!question.trim() || isLoading) return;

    setError(null);
    setShowSuggestions(false);

    // Kullanıcı mesajını ekle
    const userMessage = { role: 'user', content: question };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // API'ye istek at
      const response = await sendChatMessage(question);

      // Bot cevabını ekle
      const botMessage = {
        role: 'bot',
        content: response.answer,
        sources: response.sources,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setError(err.message);

      // Hata mesajını ekle
      const errorMessage = {
        role: 'bot',
        content: `Üzgünüm, bir hata oluştu: ${err.message}`,
        sources: [],
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading]);

  /**
   * Sohbeti temizle
   */
  const clearChat = useCallback(() => {
    setMessages([
      {
        role: 'bot',
        content: 'Merhaba! Ben Türk Mevzuat Asistanı. Kanunlar ve yönetmelikler hakkında bana soru sorabilirsin.',
        sources: [],
      },
    ]);
    setShowSuggestions(true);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    showSuggestions,
    sendMessage,
    clearChat,
    setShowSuggestions,
  };
};

export default useChat;

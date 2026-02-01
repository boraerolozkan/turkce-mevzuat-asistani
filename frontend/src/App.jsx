import { useState } from 'react';
import { Send } from 'lucide-react';
import { ChatWindow } from './components';
import useChat from './hooks/useChat';
import './App.css';

function App() {
  const [input, setInput] = useState('');

  // Custom hook'u kullan
  const {
    messages,
    isLoading,
    showSuggestions,
    sendMessage,
    setShowSuggestions
  } = useChat();

  // Mesaj gönderme işleyicisi
  const handleSend = (questionText) => {
    const userMessage = questionText || input;
    if (!userMessage.trim()) return;

    setInput('');
    setShowSuggestions(false);
    sendMessage(userMessage);
  };

  // Enter tuşu işleyicisi
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSend();
  };

  // Öneri sorusu tıklama işleyicisi
  const handleSuggestionClick = (question) => {
    handleSend(question);
  };

  return (
    <div className="app-container">
      {/* Üst Bilgi */}
      <header className="header">
        <h1>Mevzuat Asistanı</h1>
        <p>1000+ Kanun ve Yönetmelik Üzerinde Yapay Zeka Destekli Arama</p>
      </header>

      {/* Mesaj Alanı - Örnek sorular artık içeride */}
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        showSuggestions={showSuggestions}
        onSuggestionClick={handleSuggestionClick}
      />

      {/* Giriş Alanı */}
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Örn: Yıllık izin süresi ne kadar?"
          disabled={isLoading}
        />
        <button onClick={() => handleSend()} disabled={isLoading || !input.trim()}>
          {isLoading ? '...' : <Send size={20} />}
        </button>
      </div>
    </div>
  );
}

export default App;

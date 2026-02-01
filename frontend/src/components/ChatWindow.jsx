import { useRef, useEffect } from 'react';
import { Bot, Briefcase, ShoppingCart, Car, Home, Anchor } from 'lucide-react';
import MessageBubble from './MessageBubble';

// Örnek Sorular
const sampleQuestions = [
  {
    category: "İş Hukuku",
    icon: Briefcase,
    questions: [
      "Yıllık izin hakkı kazanmak için ne kadar süre çalışmak gerekir?",
      "Kıdem tazminatı hangi hallerde ödenir?",
      "Haftalık çalışma süresi en fazla kaç saattir?",
      "Kadın işçilerin doğum izni süreleri ne kadardır?"
    ]
  },
  {
    category: "Tüketici Hakları",
    icon: ShoppingCart,
    questions: [
      "Ayıplı mal durumunda tüketicinin seçimlik hakları nelerdir?",
      "İnternetten alınan ürünlerde cayma hakkı kaç gündür?",
      "Garanti süresi içinde arızalanan ürün için tamir süresi en fazla kaç gündür?"
    ]
  },
  {
    category: "Trafik ve Ceza",
    icon: Car,
    questions: [
      "Alkollü araç kullanmanın cezası nedir?",
      "Hız sınırını aşmanın cezası neye göre belirlenir?",
      "Ehliyetsiz araç kullanma cezası kime kesilir?"
    ]
  },
  {
    category: "Kira ve Gayrimenkul",
    icon: Home,
    questions: [
      "Kiracı evden ne zaman çıkarılabilir?",
      "Kira artış oranı neye göre belirlenir?",
      "Depozito en fazla ne kadar olabilir?"
    ]
  },
  {
    category: "Denizcilik",
    icon: Anchor,
    questions: [
      "Türk karasularında gemi kurtarma hakkı kime aittir?",
      "Yabancı gemiler Türkiye limanları arasında yolcu taşıyabilir mi?"
    ]
  }
];

/**
 * Ana sohbet penceresi bileşeni
 */
const ChatWindow = ({ messages, isLoading, showSuggestions, onSuggestionClick }) => {
  const messagesEndRef = useRef(null);

  // Her yeni mesajda sayfayı aşağı kaydır
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-window">
      {/* Mesajlar */}
      {messages.map((message, index) => (
        <MessageBubble key={index} message={message} />
      ))}

      {/* Örnek Sorular */}
      {showSuggestions && !isLoading && (
        <div className="suggestions-container">
          <div className="suggestions-title">Örnek Sorular</div>
          <div className="suggestions-grid">
            {sampleQuestions.map((category, catIndex) => (
              <div key={catIndex} className="suggestion-category">
                <div className="category-header">
                  <category.icon size={16} />
                  <span>{category.category}</span>
                </div>
                <div className="category-questions">
                  {category.questions.map((question, qIndex) => (
                    <button
                      key={qIndex}
                      className="suggestion-button"
                      onClick={() => onSuggestionClick(question)}
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Yükleniyor göstergesi */}
      {isLoading && (
        <div className="message bot">
          <div className="avatar">
            <Bot size={24} />
          </div>
          <div className="bubble">
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
            <span className="typing-dot"></span>
          </div>
        </div>
      )}

      {/* Otomatik scroll için referans noktası */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default ChatWindow;

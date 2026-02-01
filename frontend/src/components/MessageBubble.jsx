import ReactMarkdown from 'react-markdown';
import { User, Bot } from 'lucide-react';
import SourceCard from './SourceCard';

/**
 * Tek bir mesaj baloncuğu bileşeni
 */
const MessageBubble = ({ message }) => {
  const { role, content, sources, isError } = message;
  const isBot = role === 'bot';

  return (
    <div className={`message ${role}`}>
      {/* Avatar */}
      <div className="avatar">
        {isBot ? <Bot size={24} /> : <User size={24} />}
      </div>

      {/* İçerik */}
      <div className="content">
        <div className={`bubble ${isError ? 'error' : ''}`}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>

        {/* Kaynaklar (sadece bot mesajlarında) */}
        {isBot && sources && <SourceCard sources={sources} />}
      </div>
    </div>
  );
};

export default MessageBubble;

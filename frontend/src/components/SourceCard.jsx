import { BookOpen } from 'lucide-react';

/**
 * Kaynak gösterimi bileşeni
 * Cevabın hangi dokümandan alındığını gösterir
 */
const SourceCard = ({ sources }) => {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="sources">
      <div className="sources-title">
        <BookOpen size={16} />
        <span>Referans Kaynaklar</span>
      </div>

      {sources.slice(0, 2).map((source, index) => (
        <div key={index} className="source-item">
          <span className="source-name">
            {source.source.length > 50
              ? source.source.substring(0, 50) + '...'
              : source.source}
          </span>
          <div style={{ fontSize: '0.8rem', color: '#555' }}>
            "...{source.page_content.substring(0, 150)}..."
          </div>
        </div>
      ))}
    </div>
  );
};

export default SourceCard;

import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface ExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  code: string;
}

const ExportModal = ({ isOpen, onClose, code }: ExportModalProps) => {
  if (!isOpen) return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    // Could show toast here
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      background: 'rgba(0, 0, 0, 0.7)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
    }}>
      <div style={{
        background: '#2d3436',
        borderRadius: '12px',
        width: '80%',
        maxWidth: '800px',
        maxHeight: '90vh',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
        border: '1px solid #636e72',
      }}>
        {/* Header */}
        <div style={{
          padding: '16px 24px',
          borderBottom: '1px solid #636e72',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}>
          <h2 style={{ margin: 0, color: '#fff', fontSize: '1.2rem' }}>⚛️ Qiskit Export</h2>
          <button 
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: '#b2bec3',
              fontSize: '1.5rem',
              cursor: 'pointer',
            }}
          >
            &times;
          </button>
        </div>

        {/* Code Content */}
        <div style={{
          flex: 1,
          overflow: 'auto',
          padding: '0',
          background: '#282a36', // Match dracula bg
        }}>
          <SyntaxHighlighter 
            language="python" 
            style={dracula}
            customStyle={{ margin: 0, padding: '24px', fontSize: '0.9rem' }}
          >
            {code}
          </SyntaxHighlighter>
        </div>

        {/* Footer */}
        <div style={{
          padding: '16px 24px',
          borderTop: '1px solid #636e72',
          display: 'flex',
          justifyContent: 'flex-end',
          gap: '12px',
        }}>
          <button 
            onClick={onClose}
            style={{
              padding: '8px 16px',
              background: 'transparent',
              border: '1px solid #636e72',
              color: '#dfe6e9',
              borderRadius: '6px',
              cursor: 'pointer',
            }}
          >
            Close
          </button>
          <button 
            onClick={handleCopy}
            style={{
              padding: '8px 16px',
              background: '#6c5ce7',
              border: 'none',
              color: 'white',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '600',
            }}
          >
            Copy to Clipboard
          </button>
        </div>
      </div>
    </div>
  );
};

export default ExportModal;

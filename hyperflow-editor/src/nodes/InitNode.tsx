import { memo } from 'react';
import { Handle, Position, type NodeProps } from 'reactflow';

// CSS modules don't exist yet, we'll inline styles for speed then extract later
// or we can reuse HexNode styles if we want consistent shape

const InitNode = ({ data, selected }: NodeProps) => {
  return (
    <div
      style={{
        padding: '10px 20px',
        borderRadius: '8px',
        background: 'linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%)',
        color: 'white',
        border: selected ? '2px solid #fff' : '2px solid transparent',
        boxShadow: selected ? '0 0 10px rgba(108, 92, 231, 0.6)' : '0 4px 6px rgba(0,0,0,0.1)',
        minWidth: '150px',
        textAlign: 'center',
        fontFamily: 'Inter, sans-serif'
      }}
    >
      <div style={{ fontSize: '10px', textTransform: 'uppercase', opacity: 0.8, marginBottom: '4px' }}>
        Register Declaration
      </div>
      <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
        {data.label || 'q = QReg(2)'}
      </div>
      
      {/* Output Handle */}
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: '#fff', width: '10px', height: '10px' }}
      />
    </div>
  );
};

export default memo(InitNode);

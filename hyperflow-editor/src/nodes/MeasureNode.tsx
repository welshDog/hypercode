import { memo } from 'react';
import { Handle, Position, type NodeProps } from 'reactflow';

const MeasureNode = ({ data, selected }: NodeProps) => {
  return (
    <div
      style={{
        padding: '8px 16px',
        borderRadius: '20px',
        background: 'linear-gradient(135deg, #0984e3 0%, #74b9ff 100%)',
        color: 'white',
        border: selected ? '2px solid #fff' : '2px solid transparent',
        boxShadow: selected ? '0 0 10px rgba(9, 132, 227, 0.6)' : '0 4px 6px rgba(0,0,0,0.1)',
        minWidth: '120px',
        textAlign: 'center',
        fontFamily: 'Inter, sans-serif',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '8px'
      }}
    >
      <Handle
        type="target"
        position={Position.Top}
        style={{ background: '#fff', width: '8px', height: '8px' }}
      />
      
      <span style={{ fontSize: '18px' }}>⚡</span>
      <div style={{ fontWeight: 'bold', fontSize: '14px' }}>
        {data.label || 'Measure'}
      </div>
      
      {/* No output handle usually for measure, or maybe to classical output */}
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: '#dfe6e9', width: '8px', height: '8px', borderRadius: '0' }} // Square for classical
      />
    </div>
  );
};

export default memo(MeasureNode);

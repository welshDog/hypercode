import { memo } from 'react';
import { Handle, Position, type NodeProps } from 'reactflow';

const GateNode = ({ data, selected }: NodeProps) => {
  // Color coding based on gate type
  const getGateColor = (type: string) => {
    switch (type?.toLowerCase()) {
      case 'h': return 'linear-gradient(135deg, #fdcb6e 0%, #ffeaa7 100%)'; // Yellow
      case 'x': return 'linear-gradient(135deg, #ff7675 0%, #fab1a0 100%)'; // Red
      case 'z': return 'linear-gradient(135deg, #74b9ff 0%, #a29bfe 100%)'; // Blue
      case 'cx': return 'linear-gradient(135deg, #00b894 0%, #55efc4 100%)'; // Green
      default: return 'linear-gradient(135deg, #636e72 0%, #b2bec3 100%)'; // Grey
    }
  };

  const bg = getGateColor(data.gateType || 'H');
  const textColor = '#2d3436';

  return (
    <div
      style={{
        width: '60px',
        height: '60px',
        borderRadius: '12px',
        background: bg,
        color: textColor,
        border: selected ? '2px solid #2d3436' : '1px solid rgba(0,0,0,0.1)',
        boxShadow: selected ? '0 0 10px rgba(0,0,0,0.2)' : '0 2px 4px rgba(0,0,0,0.1)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontFamily: 'Inter, sans-serif',
        fontWeight: 'bold',
        fontSize: '18px',
        position: 'relative'
      }}
    >
      <Handle
        type="target"
        position={Position.Top}
        style={{ background: '#2d3436', width: '8px', height: '8px' }}
      />
      
      {data.label || data.gateType || 'H'}
      
      <Handle
        type="source"
        position={Position.Bottom}
        style={{ background: '#2d3436', width: '8px', height: '8px' }}
      />
    </div>
  );
};

export default memo(GateNode);

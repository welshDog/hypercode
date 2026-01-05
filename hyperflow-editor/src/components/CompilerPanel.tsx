import React, { useState } from 'react';
import { Panel } from 'reactflow';

interface CompilerPanelProps {
  code: string;
  simulation?: Record<string, any>;
  onClose: () => void;
}

const CompilerPanel: React.FC<CompilerPanelProps> = ({ code, simulation, onClose }) => {
  const [activeTab, setActiveTab] = useState<'code' | 'simulation'>('code');

  const renderPlasmidMap = (result: any) => {
    if (!result.parts || result.parts.length === 0) return null;

    const isCircular = result.isCircular;
    const totalLength = result.length;
    const center = 100;
    const radius = 70;
    const strokeWidth = 20;
    const colors = ['#00b894', '#0984e3', '#fdcb6e', '#e17055', '#6c5ce7', '#d63031'];

    let startAngle = 0;

    // Calculate effective lengths for visualization segments
    // We use seq length as weight
    const totalWeight = result.parts.reduce((sum: number, part: any) => sum + part.seq.length, 0);

    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '15px' }}>
        <svg width="200" height="200" viewBox="0 0 200 200">
          {result.parts.map((part: any, index: number) => {
            const weight = part.seq.length;
            const sweepAngle = (weight / totalWeight) * (isCircular ? 360 : 350); // Leave gap if linear

            // Calculate SVG arc path
            // Convert polar to cartesian
            const getCoords = (angleInDegrees: number) => {
              const angleInRadians = (angleInDegrees - 90) * Math.PI / 180.0;
              return {
                x: center + radius * Math.cos(angleInRadians),
                y: center + radius * Math.sin(angleInRadians)
              };
            };

            const start = getCoords(startAngle);
            const end = getCoords(startAngle + sweepAngle);
            const largeArcFlag = sweepAngle > 180 ? 1 : 0;

            const pathData = isCircular || index < result.parts.length
              ? [
                `M ${start.x} ${start.y}`,
                `A ${radius} ${radius} 0 ${largeArcFlag} 1 ${end.x} ${end.y}`
              ].join(' ')
              : ''; // TODO: Linear visualization logic if needed, but Arc works for linear too (just open)

            const color = colors[index % colors.length];

            // Calculate label position (midpoint angle)
            const midAngle = startAngle + sweepAngle / 2;
            const labelCoords = getCoords(midAngle);
            // Push label out a bit
            const labelX = center + (radius + 25) * Math.cos((midAngle - 90) * Math.PI / 180.0);
            const labelY = center + (radius + 25) * Math.sin((midAngle - 90) * Math.PI / 180.0);

            startAngle += sweepAngle;

            return (
              <g key={index}>
                <path
                  d={pathData}
                  fill="none"
                  stroke={color}
                  strokeWidth={strokeWidth}
                />
                <text
                  x={labelX}
                  y={labelY}
                  textAnchor="middle"
                  alignmentBaseline="middle"
                  fill="#2d3436"
                  fontSize="10"
                  fontWeight="bold"
                >
                  {part.label || `Part ${index + 1}`}
                </text>
              </g>
            );
          })}
          <text x="100" y="100" textAnchor="middle" alignmentBaseline="middle" fontSize="12" fontWeight="bold" fill="#636e72">
            {totalLength} bp
          </text>
          {!isCircular && (
            <text x="100" y="115" textAnchor="middle" fontSize="10" fill="#e17055">(Linear)</text>
          )}
        </svg>
      </div>
    );
  };

  return (
    <Panel position="bottom-center" style={{
      width: '80%',
      maxWidth: '900px',
      height: '400px',
      background: 'white',
      borderRadius: '8px',
      boxShadow: '0 -4px 30px rgba(0,0,0,0.15)',
      display: 'flex',
      flexDirection: 'column',
      overflow: 'hidden',
      border: '1px solid #e0e0e0',
      animation: 'slideUp 0.3s ease-out'
    }}>
      {/* Header */}
      <div style={{
        padding: '0 15px',
        background: '#2d3436',
        color: 'white',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        fontFamily: 'Inter, sans-serif',
        height: '50px'
      }}>
        <div style={{ display: 'flex', gap: '20px', height: '100%' }}>
          <button
            onClick={() => setActiveTab('code')}
            style={{
              background: 'transparent',
              border: 'none',
              borderBottom: activeTab === 'code' ? '3px solid #0984e3' : '3px solid transparent',
              color: activeTab === 'code' ? 'white' : '#b2bec3',
              fontWeight: 'bold',
              cursor: 'pointer',
              height: '100%',
              padding: '0 10px'
            }}
          >
            💻 Generated Code
          </button>
          <button
            onClick={() => setActiveTab('simulation')}
            style={{
              background: 'transparent',
              border: 'none',
              borderBottom: activeTab === 'simulation' ? '3px solid #00b894' : '3px solid transparent',
              color: activeTab === 'simulation' ? 'white' : '#b2bec3',
              fontWeight: 'bold',
              cursor: 'pointer',
              height: '100%',
              padding: '0 10px'
            }}
          >
            🧪 Simulation Results
          </button>
        </div>

        <button
          onClick={onClose}
          style={{
            background: 'transparent',
            border: 'none',
            color: 'white',
            cursor: 'pointer',
            fontSize: '18px'
          }}
        >
          ✕
        </button>
      </div>

      {/* Content Area */}
      <div style={{
        flex: 1,
        overflow: 'hidden',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column'
      }}>
        {activeTab === 'code' ? (
          // Code View
          <>
            <div style={{
              flex: 1,
              padding: '15px',
              overflow: 'auto',
              background: '#f5f6fa',
              fontFamily: 'monospace',
              fontSize: '14px',
              lineHeight: '1.5',
              color: '#2d3436'
            }}>
              <pre>{code}</pre>
            </div>
            <div style={{
              padding: '10px',
              borderTop: '1px solid #e0e0e0',
              display: 'flex',
              justifyContent: 'flex-end',
              background: 'white'
            }}>
              <button
                onClick={() => navigator.clipboard.writeText(code)}
                style={{
                  padding: '8px 16px',
                  background: '#0984e3',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                Copy Code
              </button>
            </div>
          </>
        ) : (
          // Simulation View
          <div style={{
            flex: 1,
            padding: '20px',
            overflow: 'auto',
            background: '#f1f2f6',
            display: 'flex',
            flexDirection: 'column',
            gap: '15px'
          }}>
            {!simulation ? (
              <div style={{ color: '#636e72', textAlign: 'center', marginTop: '40px' }}>
                No simulation data available.
              </div>
            ) : (
              Object.entries(simulation).map(([nodeId, result]) => (
                <div key={nodeId} style={{
                  background: 'white',
                  padding: '15px',
                  borderRadius: '8px',
                  boxShadow: '0 2px 5px rgba(0,0,0,0.05)',
                  borderLeft: `4px solid ${result.type === 'edited_dna' ? '#e17055' : result.type === 'amplicon' ? '#fdcb6e' : '#74b9ff'}`
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <span style={{ fontWeight: 'bold', color: '#2d3436', textTransform: 'uppercase', fontSize: '12px' }}>
                      {result.type}
                    </span>
                    {result.efficiency && (
                      <span style={{ background: '#55efc4', padding: '2px 8px', borderRadius: '10px', fontSize: '12px', fontWeight: 'bold' }}>
                        Yield: {result.efficiency}
                      </span>
                    )}
                    {result.off_target_score && (
                      <span style={{ background: '#ffeaa7', padding: '2px 8px', borderRadius: '10px', fontSize: '12px', fontWeight: 'bold' }}>
                        Off-Target: {result.off_target_score}
                      </span>
                    )}
                  </div>

                  {result.type === 'plasmid' && renderPlasmidMap(result)}

                  {result.sequence && (
                    <div style={{
                      fontFamily: 'monospace',
                      wordBreak: 'break-all',
                      background: '#dfe6e9',
                      padding: '8px',
                      borderRadius: '4px',
                      fontSize: '12px',
                      color: '#2d3436',
                      marginBottom: '10px'
                    }}>
                      {result.sequence}
                    </div>
                  )}

                  {result.log && result.log.length > 0 && (
                    <div style={{ fontSize: '12px', color: '#636e72' }}>
                      {result.log.map((entry: string, i: number) => (
                        <div key={i}>• {entry}</div>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
    </Panel>
  );
};

export default CompilerPanel;

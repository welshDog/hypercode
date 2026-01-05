import React, { useEffect, useMemo, useState } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './EnzymeNode.module.css'; // Reusing enzyme styles for consistency
import { type GoldenGateNodeData } from '../engine/BioTypes';

const GoldenGateNode: React.FC<NodeProps<GoldenGateNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const nodes = useNodes();
  const edges = useEdges();

  const [isPulse, setIsPulse] = useState(false);

  // Identify connected source nodes (parts)
  const incomingParts = useMemo(() => {
    const incomingEdges = edges.filter(e => e.target === id);
    // Sort edges by source Y position to give a visual order? Or just simple order.
    // Let's sort by Y position so top nodes are first.
    return incomingEdges
      .map(edge => {
        const node = nodes.find(n => n.id === edge.source);
        return {
          id: node?.id || '',
          data: node?.data as any,
          y: node?.position.y || 0
        };
      })
      .filter(n => n.data?.sequence)
      .sort((a, b) => a.y - b.y);
  }, [edges, nodes, id]);

  // Update internal data when inputs change
  useEffect(() => {
    const currentParts = incomingParts.map(p => ({
      id: p.id,
      name: p.data.label || 'Part',
      sequence: p.data.sequence || '',
      overhangs: { left: '????', right: '????' } // Placeholder for now, computed in backend/simulator
    }));

    // Check if parts changed
    if (JSON.stringify(currentParts) !== JSON.stringify(data.parts)) {
      setIsPulse(true);
      setTimeout(() => setIsPulse(false), 600);

      setNodes(nds => nds.map(node => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              parts: currentParts,
              // Simple client-side mock assembly visualization (just concatenation for now)
              assemblyResult: currentParts.length > 0 ? 'Ready for Assembly' : 'Waiting for parts...',
              isValid: currentParts.length >= 2
            }
          };
        }
        return node;
      }));
    }
  }, [incomingParts, id, setNodes, data.parts]);

  const handleChangeEnzyme = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const enzyme = e.target.value as any;
    setNodes(nds => nds.map(n => n.id === id ? { ...n, data: { ...n.data, enzyme } } : n));
  };

  return (
    <div className={`${styles.container} ${data.error ? styles.error : ''} ${isPulse ? styles.pulse : ''}`} style={{ borderColor: '#fdcb6e', minWidth: '200px' }}>
      <Handle type="target" position={Position.Left} className={styles.handle} style={{ background: '#fdcb6e' }} />

      <div className={styles.header} style={{ background: '#ffeaa7', color: '#d35400' }}>
        <div className={styles.icon}>🧬</div>
        <div className={styles.title}>Golden Gate Assembly</div>
      </div>

      <div className={styles.body}>
        <div className={styles.field}>
          <label>Type IIS Enzyme</label>
          <select
            className={styles.select}
            value={data.enzyme || 'BsaI'}
            onChange={handleChangeEnzyme}
          >
            <option value="BsaI">BsaI (GGTCTC)</option>
            <option value="BbsI">BbsI (GAAGAC)</option>
            <option value="BsmBI">BsmBI (CGTCTC)</option>
          </select>
        </div>

        <div className={styles.field}>
          <label>Parts Loaded: {data.parts?.length || 0}</label>
          <div style={{
            fontSize: '10px',
            background: 'rgba(0,0,0,0.05)',
            padding: '4px',
            borderRadius: '4px',
            maxHeight: '60px',
            overflowY: 'auto'
          }}>
            {data.parts && data.parts.length > 0 ? (
              data.parts.map((p, i) => (
                <div key={i} style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span>{i + 1}. {p.name}</span>
                  <span style={{ fontFamily: 'monospace' }}>{p.sequence.length}bp</span>
                </div>
              ))
            ) : (
              <span style={{ color: '#aaa', fontStyle: 'italic' }}>Connect Sequence Nodes...</span>
            )}
          </div>
        </div>

        {data.assemblyResult && (
          <div className={styles.field}>
            <label>Status</label>
            <div style={{
              fontFamily: 'monospace',
              fontSize: '10px',
              color: data.isValid ? '#27ae60' : '#e74c3c'
            }}>
              {data.isValid ? '✅ Ready to Assemble' : '⚠️ Need 2+ parts'}
            </div>
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Right} className={styles.handle} style={{ background: '#fdcb6e' }} />
    </div>
  );
};

export default GoldenGateNode;

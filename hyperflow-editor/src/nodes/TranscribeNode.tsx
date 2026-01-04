import React, { useEffect, useMemo } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './TranscribeNode.module.css';
import { type TranscribeNodeData, type SequenceNodeData } from '../engine/BioTypes';

const TranscribeNode: React.FC<NodeProps<TranscribeNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const nodes = useNodes();
  const edges = useEdges();

  // 1. Find the connected source node
  // In v11, we manually filter edges and nodes
  const sourceNodeData = useMemo(() => {
    const edge = edges.find(e => e.target === id);
    if (!edge) return undefined;
    const node = nodes.find(n => n.id === edge.source);
    return node?.data as SequenceNodeData | undefined;
  }, [edges, nodes, id]);

  const [isPulse, setIsPulse] = React.useState(false);

  // 2. Reactive Logic: Compute RNA when DNA source changes
  useEffect(() => {
    if (sourceNodeData) {
      // Check upstream validity
      if (sourceNodeData.isValid === false) {
        // Propagate error
        if (data.isValid !== false) {
          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === id) {
                return {
                  ...node,
                  data: {
                    ...node.data,
                    sequence: '', // Clear output on error
                    isValid: false,
                  },
                };
              }
              return node;
            })
          );
        }
        return;
      }

      if (sourceNodeData.sequence) {
        const dna = sourceNodeData.sequence;
        // Transcription: Replace T with U (Basic model)
        const rna = dna.replace(/T/g, 'U');

        // Only update if changed to avoid loops
        if (data.sequence !== rna) {
          // Trigger pulse
          setIsPulse(true);
          setTimeout(() => setIsPulse(false), 600);

          setNodes((nds) =>
            nds.map((node) => {
              if (node.id === id) {
                return {
                  ...node,
                  data: {
                    ...node.data,
                    sequence: rna,
                    isValid: true, // Valid if upstream is valid
                  },
                };
              }
              return node;
            })
          );
        }
      }
    } else if (!sourceNodeData && data.sequence) {
      // Reset if disconnected
      setNodes((nds) =>
        nds.map((node) => {
          if (node.id === id) {
            return {
              ...node,
              data: { ...node.data, sequence: '', isValid: true },
            };
          }
          return node;
        })
      );
    }
  }, [sourceNodeData, id, setNodes, data.sequence, data.isValid]);

  const isError = data.isValid === false;

  return (
    <div className={`${styles.container} ${isError ? styles.error : ''} ${isPulse ? styles.pulse : ''}`}>
      <Handle type="target" position={Position.Left} className={styles.handle} />

      <div className={styles.header}>
        <span>{isError ? '⚠️' : '🌫️'}</span> Transcribe
      </div>

      <div className={styles.body}>
        <div className={styles.preview}>
          {isError ? 'Upstream Error' : (data.sequence || '')}
        </div>

        <div className={styles.stats}>
          <span>Length: {isError ? 0 : (data.sequence?.length || 0)} nt</span>
          <span>Type: mRNA</span>
        </div>
      </div>

      <Handle type="source" position={Position.Right} className={styles.handle} />
    </div>
  );
};

export default TranscribeNode;

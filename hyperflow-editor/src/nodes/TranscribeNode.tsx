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
        let rna = '';

        // Handle Strand Selection
        if (data.isCodingStrand === false) {
          // Template Strand: Complement then replace T->U
          // A->U, T->A, G->C, C->G
          // Reverse complement if reading 3'->5'?
          // Standard convention: User inputs 5'->3' template strand.
          // mRNA is complementary and antiparallel.
          // For simplicity in this tool: "Template Strand" means we take the complement.
          rna = dna.split('').map(base => {
            switch (base) {
              case 'A': return 'U';
              case 'T': return 'A';
              case 'G': return 'C';
              case 'C': return 'G';
              default: return base;
            }
          }).join('');
        } else {
          // Coding Strand (Default): Just replace T->U
          rna = dna.replace(/T/g, 'U');
        }

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
        <div className={styles.row}>
          <label className={styles.label}>Strand:</label>
          <select
            className={styles.select}
            value={data.isCodingStrand !== false ? 'coding' : 'template'}
            onChange={(e) => {
              const isCoding = e.target.value === 'coding';
              setNodes(nds => nds.map(n => {
                if (n.id === id) {
                  return { ...n, data: { ...n.data, isCodingStrand: isCoding } };
                }
                return n;
              }));
            }}
          >
            <option value="coding">Coding (5'→3')</option>
            <option value="template">Template (3'→5')</option>
          </select>
        </div>

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

import React, { useEffect, useMemo, useState } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './CRISPRNode.module.css';
import { type CRISPRNodeData, type SequenceNodeData } from '../engine/BioTypes';

const CRISPRNode: React.FC<NodeProps<CRISPRNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const nodes = useNodes();
  const edges = useEdges();

  // 1. Get Upstream DNA
  const sourceNodeData = useMemo(() => {
    const edge = edges.find(e => e.target === id);
    if (!edge) return undefined;
    const node = nodes.find(n => n.id === edge.source);
    // Can accept DNA from Sequence, Enzyme, Ligase
    // For simplicity, checking if it has a 'sequence' field and type 'DNA'
    if (node && (node.data as any).type === 'DNA') {
      return node.data as SequenceNodeData;
    }
    return undefined;
  }, [edges, nodes, id]);

  const [gRNA, setGRNA] = useState(data.guideRNA || '');
  const [pam, setPAM] = useState(data.pam || 'NGG');

  // 2. Search Logic
  useEffect(() => {
    if (sourceNodeData && sourceNodeData.sequence) {
      const dna = sourceNodeData.sequence.toUpperCase();
      const currentGRNA = (data.guideRNA || '').toUpperCase();
      const currentPAM = (data.pam || 'NGG').toUpperCase();

      if (!currentGRNA || currentGRNA.length < 10) {
        // Too short to match reliably
         if (data.isOnTarget) {
             updateNodeData(false, -1);
         }
         return;
      }

      // Convert PAM to Regex (N -> .)
      const pamRegexStr = currentPAM.replace(/N/g, '.');
      // Full target: gRNA + PAM
      const targetRegex = new RegExp(`${currentGRNA}${pamRegexStr}`, 'g');
      
      const match = targetRegex.exec(dna);
      const isMatch = !!match;
      const index = match ? match.index : -1;

      if (isMatch !== data.isOnTarget || index !== data.matchIndex) {
         updateNodeData(isMatch, index);
      }
    } else {
        // Reset if no input
        if (data.isOnTarget) {
            updateNodeData(false, -1);
        }
    }
  }, [sourceNodeData, data.guideRNA, data.pam, id]);

  const updateNodeData = (isOnTarget: boolean, matchIndex: number) => {
    setNodes(nds => nds.map(n => {
        if (n.id === id) {
            return { ...n, data: { ...n.data, isOnTarget, matchIndex } };
        }
        return n;
    }));
  };

  // UI Handlers
  const handleGRNAChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = e.target.value;
      setGRNA(val);
      // Debounce or direct update? Direct for now, but update node data
      setNodes(nds => nds.map(n => {
        if (n.id === id) {
            return { ...n, data: { ...n.data, guideRNA: val } };
        }
        return n;
      }));
  };

  const handlePAMChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = e.target.value;
      setPAM(val);
      setNodes(nds => nds.map(n => {
        if (n.id === id) {
            return { ...n, data: { ...n.data, pam: val } };
        }
        return n;
      }));
  };

  return (
    <div className={`${styles.container} ${(data as any).className || ''}`}>
      <Handle type="target" position={Position.Left} className={styles.handle} />
      
      <div className={styles.header}>
        <span>✂️</span> CRISPR-Cas9
      </div>

      <div className={styles.body}>
        <div className={styles.inputGroup}>
            <label className={styles.label}>Guide RNA (5'→3')</label>
            <input 
                className={styles.input} 
                value={gRNA} 
                onChange={handleGRNAChange}
                placeholder="e.g. GACTG..." 
            />
        </div>
        <div className={styles.inputGroup}>
            <label className={styles.label}>PAM Sequence</label>
            <input 
                className={styles.input} 
                value={pam} 
                onChange={handlePAMChange}
                placeholder="NGG" 
            />
        </div>

        {sourceNodeData ? (
            <div className={`${styles.result} ${data.isOnTarget ? styles.match : styles.noMatch}`}>
                {data.isOnTarget 
                    ? `✅ Target Found at index ${data.matchIndex}` 
                    : `❌ No target site found`}
            </div>
        ) : (
            <div className={styles.result}>Waiting for DNA...</div>
        )}
      </div>

      <Handle type="source" position={Position.Right} className={styles.handle} />
    </div>
  );
};

export default CRISPRNode;

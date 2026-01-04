import React, { useState, useEffect, useCallback } from 'react';
import { Handle, Position, type NodeProps, useReactFlow } from 'reactflow';
import styles from './SequenceNode.module.css';
import { type SequenceNodeData } from '../engine/BioTypes';

const SequenceNode: React.FC<NodeProps<SequenceNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const [sequence, setSequence] = useState(data.sequence || '');
  const [isValid, setIsValid] = useState(data.isValid ?? true);
  const [gcContent, setGcContent] = useState(data.gcContent || 0);

  // Validate and stats calculation
  const validateAndStats = useCallback((seq: string) => {
    // Regex: Only A, T, C, G (case insensitive)
    // Allowing whitespace for formatting, but stripping it for logic
    const cleanSeq = seq.replace(/\s/g, '').toUpperCase();
    const valid = /^[ATGC]*$/.test(cleanSeq);

    setIsValid(valid);

    let newGc = 0;
    if (valid && cleanSeq.length > 0) {
      const gcCount = (cleanSeq.match(/[GC]/g) || []).length;
      newGc = Math.round((gcCount / cleanSeq.length) * 100);
      setGcContent(newGc);
    } else {
      setGcContent(0);
    }

    // Update node data (propagating to the graph)
    // using setNodes to ensure reactivity
    setNodes((nodes) =>
      nodes.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: {
              ...node.data,
              sequence: cleanSeq,
              isValid: valid,
              length: cleanSeq.length,
              gcContent: newGc,
            },
          };
        }
        return node;
      })
    );
  }, [id, setNodes]);

  const handleChange = (evt: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = evt.target.value;
    setSequence(val);
    validateAndStats(val);
  };

  // Initial check
  useEffect(() => {
    validateAndStats(sequence);
  }, []);

  return (
    <div className={`${styles.container} ${!isValid ? styles.error : ''}`}>
      <div className={styles.header}>
        <span className={styles.icon}>🧬</span>
        DNA Sequence
      </div>

      <textarea
        className={`${styles.textarea} ${!isValid ? styles.invalid : ''}`}
        value={sequence}
        onChange={handleChange}
        placeholder="Enter ATGC sequence..."
        spellCheck={false}
      />

      {/* Validation Message */}
      {!isValid && (
        <div className={styles.errorMsg}>
          ⚠️ Invalid Nucleotides Detected
        </div>
      )}

      {/* Stats Panel */}
      <div className={styles.stats}>
        <span>Length: {sequence.replace(/\s/g, '').length} bp</span>
        <span>GC: {gcContent}%</span>
      </div>

      {/* Output Handle (Source) */}
      <Handle
        type="source"
        position={Position.Right}
        id="out"
        className={styles.handle}
      />
    </div>
  );
};

export default SequenceNode;

import React, { useState, useEffect } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './PCRNode.module.css';
import { type PCRNodeData } from '../engine/BioTypes';
import { calculateTm, performPCR } from '../engine/PCRUtils';

const PCRNode: React.FC<NodeProps<PCRNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const edges = useEdges();
  const nodes = useNodes();

  // Local state for inputs
  const [fwdPrimer, setFwdPrimer] = useState(data.forwardPrimer || '');
  const [revPrimer, setRevPrimer] = useState(data.reversePrimer || '');

  // Inputs from Upstream
  const connection = edges.find(edge => edge.target === id);
  const upstreamNode = connection ? nodes.find(n => n.id === connection.source) : null;
  const templateDNA = (upstreamNode as any)?.data?.sequence || '';

  // Calculate Logic
  useEffect(() => {
    // 1. Calculate Tms
    const fwdTm = calculateTm(fwdPrimer);
    const revTm = calculateTm(revPrimer);

    // 2. Run PCR if we have a template
    let amplicon = '';
    let error = '';

    if (templateDNA && fwdPrimer && revPrimer) {
      const result = performPCR(templateDNA, fwdPrimer, revPrimer);
      if (result.error) {
        error = result.error;
      } else {
        amplicon = result.amplicon;
      }
    } else if (!templateDNA) {
      error = 'Waiting for Template DNA...';
    }

    // 3. Update Node Data (if changed)
    // Only update if something actually changed to avoid infinite loops
    if (
      amplicon !== data.amplicon ||
      error !== data.error ||
      fwdTm !== data.forwardTm ||
      revTm !== data.reverseTm
    ) {
      setNodes((nodes) =>
        nodes.map((node) => {
          if (node.id === id) {
            return {
              ...node,
              data: {
                ...node.data,
                forwardPrimer: fwdPrimer,
                reversePrimer: revPrimer,
                amplicon,
                forwardTm: fwdTm,
                reverseTm: revTm,
                error,
                sequence: amplicon // Important: set 'sequence' so downstream nodes see it as DNA!
              },
            };
          }
          return node;
        })
      );
    }
  }, [id, fwdPrimer, revPrimer, templateDNA, setNodes, data.amplicon, data.error, data.forwardTm, data.reverseTm]);

  return (
    <div className={`${styles.container} ${data.error && templateDNA ? styles.error : ''}`}>
      <div className={styles.header}>
        <span className={styles.icon}>🌡️</span>
        PCR Thermocycler
      </div>

      {/* Target Handle (Template DNA) */}
      <Handle
        type="target"
        position={Position.Left}
        id="template"
        className={`${styles.handle} ${styles.handleIn}`}
      />

      {/* Forward Primer Input */}
      <div className={styles.section}>
        <label className={styles.label}>Forward Primer (5' → 3')</label>
        <input
          className={styles.input}
          value={fwdPrimer}
          onChange={(e) => setFwdPrimer(e.target.value)}
          placeholder="e.g. ATGC..."
        />
        <div className={styles.meta}>
          <span>Tm: {data.forwardTm}°C</span>
          <span>Len: {fwdPrimer.length}bp</span>
        </div>
      </div>

      {/* Reverse Primer Input */}
      <div className={styles.section}>
        <label className={styles.label}>Reverse Primer (5' → 3')</label>
        <input
          className={styles.input}
          value={revPrimer}
          onChange={(e) => setRevPrimer(e.target.value)}
          placeholder="e.g. GCAT..."
        />
        <div className={styles.meta}>
          <span>Tm: {data.reverseTm}°C</span>
          <span>Len: {revPrimer.length}bp</span>
        </div>
      </div>

      {/* Result Panel */}
      <div className={styles.result}>
        <span className={styles.resultLabel}>
          {data.amplicon ? '✅ Amplicon Generated' : '⚠️ Status'}
        </span>

        {data.error ? (
          <div className={styles.errorMsg}>{data.error}</div>
        ) : (
          <div className={styles.resultValue}>
            {data.amplicon.length} bp Product
            <br />
            <span style={{ opacity: 0.7, fontSize: '9px' }}>{data.amplicon.substring(0, 10)}...</span>
          </div>
        )}
      </div>

      {/* Source Handle (Amplicon Output) */}
      <Handle
        type="source"
        position={Position.Right}
        id="product"
        className={`${styles.handle} ${styles.handleOut}`}
      />
    </div>
  );
};

export default PCRNode;


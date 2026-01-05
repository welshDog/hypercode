import React, { useState, useEffect } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './CRISPRNode.module.css';
import { type CRISPRNodeData } from '../engine/BioTypes';
import { performCRISPR } from '../engine/CRISPRLogic';

const CRISPRNode: React.FC<NodeProps<CRISPRNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const edges = useEdges();
  const nodes = useNodes();

  // Local state
  const [guideRNA, setGuideRNA] = useState(data.guideRNA || '');
  const [pam, setPam] = useState(data.pam || 'NGG');
  const [repairMode, setRepairMode] = useState<'NHEJ' | 'HDR'>(data.repairMode || 'NHEJ');
  const [repairTemplate, setRepairTemplate] = useState(data.repairTemplate || '');

  // Inputs from Upstream
  // Assuming single target input
  const connection = edges.find(edge => edge.target === id);
  const upstreamNode = connection ? nodes.find(n => n.id === connection.source) : null;

  // Check if upstream data has 'sequence' or 'editedSequence' or 'amplicon'
  // We need a standard 'sequence' field for DNA.
  const targetDNA = (upstreamNode as any)?.data?.sequence ||
    (upstreamNode as any)?.data?.amplicon ||
    (upstreamNode as any)?.data?.editedSequence || '';

  // Logic
  useEffect(() => {
    let edited = '';
    let status: 'scanning' | 'cut' | 'repaired' | 'error' = 'scanning';
    let message = '';
    let cutIndex = -1;

    if (targetDNA) {
      const result = performCRISPR(targetDNA, guideRNA, pam, repairMode, repairTemplate);
      edited = result.editedSequence;
      status = result.status;
      message = result.message || '';
      cutIndex = result.cutIndex;
    } else {
      status = 'scanning';
      message = 'Waiting for DNA...';
    }

    // Update Node Data if changed
    if (
      edited !== data.editedSequence ||
      status !== data.status ||
      message !== data.message ||
      cutIndex !== data.cutIndex ||
      guideRNA !== data.guideRNA ||
      pam !== data.pam ||
      repairMode !== data.repairMode ||
      repairTemplate !== data.repairTemplate
    ) {
      setNodes((nodes) =>
        nodes.map((node) => {
          if (node.id === id) {
            return {
              ...node,
              data: {
                ...node.data,
                guideRNA,
                pam,
                repairMode,
                repairTemplate,
                editedSequence: edited,
                status,
                errorMessage: message,
                cutIndex,
                sequence: edited // Standard output for next node
              },
            };
          }
          return node;
        })
      );
    }
  }, [id, guideRNA, pam, repairMode, repairTemplate, targetDNA, setNodes, data]);

  return (
    <div className={`${styles.container} ${styles[data.status] || ''}`}>
      <div className={styles.header}>
        <span className={styles.icon}>🧬✂️</span>
        CRISPR/Cas9 Editor
      </div>

      <Handle
        type="target"
        position={Position.Left}
        id="target-dna"
        className={`${styles.handle} ${styles.handleIn}`}
      />

      {/* Guide RNA Section */}
      <div className={styles.section}>
        <label className={styles.label}>Guide RNA (20nt)</label>
        <input
          className={styles.input}
          value={guideRNA}
          onChange={(e) => setGuideRNA(e.target.value)}
          placeholder="Sequence upstream of PAM..."
        />
      </div>

      {/* PAM Section */}
      <div className={styles.section}>
        <label className={styles.label}>PAM Sequence</label>
        <input
          className={styles.input}
          value={pam}
          onChange={(e) => setPam(e.target.value)}
          placeholder="e.g. NGG"
        />
      </div>

      {/* Repair Mode Toggle */}
      <div className={styles.section}>
        <label className={styles.label}>Repair Mechanism</label>
        <div className={styles.modeToggle}>
          <button
            className={`${styles.modeBtn} ${repairMode === 'NHEJ' ? styles.active : ''}`}
            onClick={() => setRepairMode('NHEJ')}
          >
            NHEJ (Knockout)
          </button>
          <button
            className={`${styles.modeBtn} ${repairMode === 'HDR' ? styles.active : ''}`}
            onClick={() => setRepairMode('HDR')}
          >
            HDR (Edit)
          </button>
        </div>

        {repairMode === 'HDR' && (
          <div style={{ marginTop: '8px' }}>
            <label className={styles.label}>Repair Template</label>
            <input
              className={styles.input}
              value={repairTemplate}
              onChange={(e) => setRepairTemplate(e.target.value)}
              placeholder="Sequence to insert..."
            />
          </div>
        )}
      </div>

      {/* Status Footer */}
      <div className={`${styles.status} ${data.status === 'repaired' ? styles.success : ''} ${data.status === 'error' ? styles.error : ''}`}>
        <span className={styles.statusText}>
          {data.status === 'scanning' && 'Scanning...'}
          {data.status === 'repaired' && 'EDIT COMPLETE'}
          {data.status === 'error' && 'TARGET NOT FOUND'}
        </span>
        {data.cutIndex != null && data.cutIndex > -1 && <span style={{ fontSize: '0.65rem', opacity: 0.7 }}>Cut @ {data.cutIndex}</span>}
      </div>

      <Handle
        type="source"
        position={Position.Right}
        id="edited-dna"
        className={`${styles.handle} ${styles.handleOut}`}
      />
    </div>
  );
};

export default CRISPRNode;

import React, { useEffect, useMemo } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './LigaseNode.module.css';
import { type LigaseNodeData, type EnzymeNodeData } from '../engine/BioTypes';
import { checkLigationCompatibility, type Fragment } from '../engine/BioLogic';

const LigaseNode: React.FC<NodeProps<LigaseNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const nodes = useNodes();
  const edges = useEdges();

  // Find upstream EnzymeNode
  const upstreamNode = useMemo(() => {
    const edge = edges.find(e => e.target === id);
    if (!edge) return undefined;
    return nodes.find(n => n.id === edge.source);
  }, [edges, nodes, id]);

  const fragments = useMemo(() => {
    if (!upstreamNode) return [];
    // We assume upstream is EnzymeNode, but it could be others if we expand.
    // For now, check if it has 'fragments' in data.
    const d = upstreamNode.data as Partial<EnzymeNodeData>;
    if (d && Array.isArray(d.fragments)) {
      // Map EnzymeNodeData fragments to BioLogic Fragment type
      // We need to be careful: EnzymeNodeData fragments don't have 'id' or 'sourceEnzyme' usually
      // But BioLogic needs them? Actually checkLigationCompatibility only needs overrides
      // Let's create a partial/mock Fragment object
      return d.fragments.map((f, i) => ({
        ...f,
        id: `frag-${i}`,
        sourceEnzyme: 'unknown'
      })) as Fragment[];
    }
    return [];
  }, [upstreamNode]);

  const [isPulse, setIsPulse] = React.useState(false);

  const setData = (patch: Partial<LigaseNodeData>) => {
    setNodes(nds => nds.map(node => node.id === id ? { ...node, data: { ...node.data, ...patch } } : node));
  };

  useEffect(() => {
    if (fragments.length === 0) {
      if (data.isValid) setData({ isValid: false, ligatedSequence: '', errorMessage: 'No fragments found' });
      return;
    }

    // Default selection if nothing selected
    let leftIdx = data.selectedLeftFragmentIndex;
    let rightIdx = data.selectedRightFragmentIndex;

    // If indices are invalid/null, try to pick first two compatible ones or just 0 and 1
    if (leftIdx === null || leftIdx === undefined || leftIdx >= fragments.length) leftIdx = 0;
    if (rightIdx === null || rightIdx === undefined || rightIdx >= fragments.length) rightIdx = Math.min(1, fragments.length - 1);

    const leftFrag = fragments[leftIdx];
    const rightFrag = fragments[rightIdx];

    let isValid = false;
    let ligatedSequence = '';
    let errorMessage = '';

    if (leftFrag && rightFrag) {
      // Use BioLogic engine
      const result = checkLigationCompatibility(leftFrag, rightFrag, !!data.circular);

      isValid = result.isValid;
      ligatedSequence = result.sequence;
      errorMessage = result.error || '';
    }

    const changed = data.selectedLeftFragmentIndex !== leftIdx ||
      data.selectedRightFragmentIndex !== rightIdx ||
      data.ligatedSequence !== ligatedSequence ||
      data.isValid !== isValid ||
      data.errorMessage !== errorMessage; // Track error message change

    if (changed) {
      if (isValid) {
        setIsPulse(true);
        setTimeout(() => setIsPulse(false), 600);
      }
      setData({
        selectedLeftFragmentIndex: leftIdx,
        selectedRightFragmentIndex: rightIdx,
        ligatedSequence,
        isValid,
        errorMessage
      });
    }
  }, [fragments, data.selectedLeftFragmentIndex, data.selectedRightFragmentIndex, data.isValid, data.ligatedSequence, data.errorMessage, data.circular, id, setNodes]);

  const handleLeftChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setData({ selectedLeftFragmentIndex: parseInt(e.target.value, 10) });
  };

  const handleRightChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setData({ selectedRightFragmentIndex: parseInt(e.target.value, 10) });
  };

  const handleCircularChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setData({ circular: e.target.checked });
  };

  const renderOption = (frag: { seq: string, leftOverhang?: string, rightOverhang?: string }, idx: number) => {
    const start = frag.seq.substring(0, 4);
    const end = frag.seq.substring(frag.seq.length - 4);
    const mid = frag.seq.length > 8 ? '...' : '';
    const seqDisplay = `${start}${mid}${end}`;
    const left = frag.leftOverhang ? `(${frag.leftOverhang})` : '';
    const right = frag.rightOverhang ? `(${frag.rightOverhang})` : '';
    return `Frag ${idx}: ${left}${seqDisplay}${right}`;
  };

  const isError = !data.isValid;

  return (
    <div className={`${styles.container} ${isError ? styles.error : ''} ${isPulse ? styles.pulse : ''} ${data.circular && !isError ? styles.circular : ''}`}>
      <Handle type="target" position={Position.Left} className={styles.handle} />
      <div className={styles.header}><span>🧬</span> Ligase</div>
      <div className={styles.body}>
        <div className={styles.selectGroup}>
          <span className={styles.label}>Left Fragment (5')</span>
          <select className={styles.select} value={data.selectedLeftFragmentIndex ?? ''} onChange={handleLeftChange}>
            {fragments.map((f, i) => (
              <option key={i} value={i}>{renderOption({ seq: f.seq, leftOverhang: f.leftOverhang ?? undefined, rightOverhang: f.rightOverhang ?? undefined }, i)}</option>
            ))}
          </select>
        </div>
        <div className={styles.selectGroup}>
          <span className={styles.label}>Right Fragment (3')</span>
          <select className={styles.select} value={data.selectedRightFragmentIndex ?? ''} onChange={handleRightChange}>
            {fragments.map((f, i) => (
              <option key={i} value={i}>{renderOption({ seq: f.seq, leftOverhang: f.leftOverhang ?? undefined, rightOverhang: f.rightOverhang ?? undefined }, i)}</option>
            ))}
          </select>
        </div>

        <div className={styles.row} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <input
            type="checkbox"
            id={`circular-${id}`}
            checked={!!data.circular}
            onChange={handleCircularChange}
            style={{ cursor: 'pointer' }}
          />
          <label htmlFor={`circular-${id}`} className={styles.label} style={{ cursor: 'pointer' }}>Circularize</label>
        </div>

        {isError && <div className={styles.errorText}>{data.errorMessage}</div>}

        <div className={styles.preview}>
          {data.ligatedSequence ? data.ligatedSequence : 'No Product'}
        </div>
      </div>
      <Handle type="source" position={Position.Right} className={styles.handle} />
    </div>
  );
};

export default LigaseNode;

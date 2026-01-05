import React, { useEffect, useMemo } from 'react';
import { Handle, Position, type NodeProps, useReactFlow, useNodes, useEdges } from 'reactflow';
import styles from './EnzymeNode.module.css';
import { type EnzymeNodeData, type SequenceNodeData } from '../engine/BioTypes';
import { ENZYMES, computeRestriction } from '../engine/BioLogic';

const EnzymeNode: React.FC<NodeProps<EnzymeNodeData>> = ({ id, data }) => {
  const { setNodes } = useReactFlow();
  const nodes = useNodes();
  const edges = useEdges();

  const sourceNodeData = useMemo(() => {
    const edge = edges.find(e => e.target === id);
    if (!edge) return undefined;
    const node = nodes.find(n => n.id === edge.source);
    return node?.data as SequenceNodeData | undefined;
  }, [edges, nodes, id]);

  const [isPulse, setIsPulse] = React.useState(false);

  const setData = (patch: Partial<EnzymeNodeData>) => {
    setNodes(nds => nds.map(node => node.id === id ? { ...node, data: { ...node.data, ...patch } } : node));
  };

  useEffect(() => {
    if (sourceNodeData) {
      if (sourceNodeData.isValid === false) {
        if (data.isValid !== false) setData({ isValid: false, fragments: [], sites: [] });
        return;
      }
      const seq = (sourceNodeData.sequence || '').toUpperCase();
      if (seq.length) {
        const enzymeName = data.enzyme || 'EcoRI';
        const mode = data.mode || 'all';

        // Use BioLogic engine
        const logicFragments = computeRestriction(seq, enzymeName, mode);

        // Map engine fragments to UI fragments format
        // The engine returns {id, seq, leftOverhang, rightOverhang, sourceEnzyme}
        // The UI expects {seq, leftOverhang, rightOverhang} (BioTypes.ts is lenient on extra props, but let's be safe)
        const uiFragments = logicFragments.map(f => ({
          seq: f.seq,
          leftOverhang: f.leftOverhang || undefined,
          rightOverhang: f.rightOverhang || undefined
        }));

        // Re-calculate sites for visualization (BioLogic currently returns fragments, let's just infer site count for now or update BioLogic later to return sites too)
        // Actually, for now let's just re-implement site finding locally or rely on fragments length-1
        // The previous code returned `sites`. Let's just quick-calc sites for visual markers if needed.
        // Or better: update BioLogic to return sites.
        // Wait, I see I defined `sites` in EnzymeNodeData.
        // Let's do a quick local calc for `sites` to keep the UI markers working.
        const enzyme = ENZYMES[enzymeName];
        const sites: number[] = [];
        if (enzyme) {
          let pos = seq.indexOf(enzyme.motif);
          while (pos !== -1) {
            sites.push(pos); // Store start index of motif
            pos = seq.indexOf(enzyme.motif, pos + 1);
          }
        }
        const usedSites = mode === 'first' && sites.length > 0 ? [sites[0]] : sites;


        const changed = JSON.stringify(data.fragments || []) !== JSON.stringify(uiFragments) ||
          JSON.stringify(data.sites || []) !== JSON.stringify(usedSites) ||
          data.enzyme !== enzymeName;

        if (changed) {
          setIsPulse(true);
          setTimeout(() => setIsPulse(false), 600);
          setData({ fragments: uiFragments, sites: usedSites, isValid: true, enzyme: enzymeName, mode });
        }
      }
    } else {
      if ((data.fragments && data.fragments.length > 0) || (data.sites && data.sites.length > 0)) {
        setData({ fragments: [], sites: [], isValid: true });
      }
    }
  }, [sourceNodeData, id, setNodes, data.fragments, data.sites, data.enzyme, data.mode, data.isValid]);

  const isError = data.isValid === false;

  const handleEnzymeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setData({ enzyme: e.target.value });
  };
  const handleModeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setData({ mode: e.target.value as 'first' | 'all' });
  };

  const preview = (data.fragments || []).map((f) => {
    const left = f.leftOverhang ? `(${f.leftOverhang})` : '';
    const right = f.rightOverhang ? `(${f.rightOverhang})` : '';
    return `${left}${f.seq}${right}`;
  }).join(' | ');

  return (
    <div className={`${styles.container} ${isError ? styles.error : ''} ${isPulse ? styles.pulse : ''}`}>
      <Handle type="target" position={Position.Left} className={styles.handle} />
      <div className={styles.header}><span>{isError ? '⚠️' : '✂️'}</span> Restriction Enzyme</div>
      <div className={styles.body}>
        <div className={styles.row}>
          <select className={styles.select} value={data.enzyme || 'EcoRI'} onChange={handleEnzymeChange}>
            {Object.keys(ENZYMES).map(e => (
              <option key={e} value={e}>{e}</option>
            ))}
          </select>
          <select className={styles.select} value={data.mode || 'all'} onChange={handleModeChange}>
            <option value="all">Cut all</option>
            <option value="first">First site only</option>
          </select>
        </div>
        <div className={styles.preview}>{isError ? 'Upstream Error' : preview}</div>
        <div className={styles.stats}>
          <span>Sites: {(data.sites || []).length}</span>
          <span>Fragments: {(data.fragments || []).length}</span>
        </div>
      </div>
      <Handle type="source" position={Position.Right} className={styles.handle} />
    </div>
  );
};

export default EnzymeNode;

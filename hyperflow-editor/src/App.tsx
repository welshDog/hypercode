import { useCallback, useState, useEffect } from 'react';
import ReactFlow, {
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  type Connection as RFConnection,
  addEdge,
  type NodeTypes,
  type EdgeTypes,
  Panel,
} from 'reactflow';

import HexNode from './nodes/HexNode';
import SequenceNode from './nodes/SequenceNode';
import TranscribeNode from './nodes/TranscribeNode';
import TranslateNode from './nodes/TranslateNode';
import EnzymeNode from './nodes/EnzymeNode';
import LigaseNode from './nodes/LigaseNode';
import QuantumEdge from './edges/QuantumEdge';
import HelixEdge from './edges/HelixEdge';
import { generateQiskitCode } from './engine/QiskitExporter';
import { generateBioPythonCode } from './engine/BioPythonExporter';
import ExportModal from './components/ExportModal';
import { QUANTUM_PRESET, CENTRAL_DOGMA_PRESET, RESTRICTION_ENZYME_PRESET, type Preset } from './presets';

// --- React Flow Types ---
const nodeTypes: NodeTypes = {
  hex: HexNode,
  sequence: SequenceNode,
  transcribe: TranscribeNode,
  translate: TranslateNode,
  enzyme: EnzymeNode,
  ligase: LigaseNode,
};

const edgeTypes: EdgeTypes = {
  quantum: QuantumEdge,
  helix: HelixEdge,
};

// --- Main Component ---
function App() {
  // React Flow State
  const [nodes, setNodes, onNodesChange] = useNodesState(CENTRAL_DOGMA_PRESET.nodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(CENTRAL_DOGMA_PRESET.edges);

  // Focus Flow State
  const [zoomLevel, setZoomLevel] = useState(1);
  const [isHyperfocus, setIsHyperfocus] = useState(false);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  // Export Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [exportCode, setExportCode] = useState('');

  const loadPreset = (preset: Preset) => {
    // Reset graph with new preset
    setNodes([...preset.nodes]);
    setEdges([...preset.edges]);
  };

  const handleExport = () => {
    const code = generateQiskitCode(nodes, edges);
    setExportCode(code);
    setIsModalOpen(true);
  };

  const handleBioExport = () => {
    // Filter for Bio-Lane nodes only (simple heuristic based on type)
    const bioNodes = nodes.filter(n => ['sequence', 'transcribe', 'translate', 'enzyme', 'ligase'].includes(n.type || ''));
    const code = generateBioPythonCode(bioNodes, edges);
    setExportCode(code);
    setIsModalOpen(true);
  };

  const onConnect = useCallback((params: RFConnection) => setEdges((eds) => addEdge(params, eds)), [setEdges]);

  // Focus Flow Logic
  const handleMove = useCallback((_e: any, viewport: { zoom: number }) => {
    setZoomLevel(viewport.zoom);
  }, []);

  const handleSelectionChange = useCallback(({ nodes: selectedNodes }: { nodes: import('reactflow').Node[] }) => {
    if (selectedNodes.length > 0) {
      setSelectedNodeId(selectedNodes[0].id);
    } else {
      setSelectedNodeId(null);
    }
  }, []);

  // Determine classes for the container
  const isLodLow = zoomLevel < 0.6;
  const containerClass = `hyperflow-container ${isLodLow ? 'lod-low' : ''} ${isHyperfocus ? 'hyperfocus-mode' : ''}`;

  // Apply dimming logic
  // We don't want to re-render nodes constantly, but we can use CSS variables or classes
  // A cleaner way for "Hyperfocus" is to pass a class to the ReactFlow wrapper, and use CSS to select dimmed nodes
  // But we need to know WHICH nodes are dimmed.
  // We can update the nodes' className when selection changes if hyperfocus is on.

  // Actually, let's update node classes whenever selection/hyperfocus changes
  // This might be slightly expensive but for <100 nodes it's fine.

  const getFocusSet = (centerId: string | null) => {
    if (!centerId) return new Set<string>();
    const focusSet = new Set<string>();
    focusSet.add(centerId);
    // Add neighbors
    edges.forEach(edge => {
      if (edge.source === centerId) focusSet.add(edge.target);
      if (edge.target === centerId) focusSet.add(edge.source);
    });
    return focusSet;
  };

  // Effect to update node styles for Hyperfocus
  // We use a useEffect to avoid loop in render
  useState(() => {
    // This is just initialization, real logic in useEffect
  });

  // We need to use `setNodes` to update classNames. 
  // To avoid infinite loop, we should only do this when specific dependencies change.
  // Actually, let's just use inline styles or classes in the render logic if possible? 
  // No, ReactFlow controls the node rendering. We have to update the node objects.

  // Optimization: Only update if the state actually changes.
  // Better yet: Use a computed style map or Context?
  // Let's stick to the className update for now, triggered by effects.

  // NOTE: In a real large app, we'd use a custom node wrapper that listens to a context.
  // For this v1.2, let's use the className approach.

  const updateNodeDimming = useCallback(() => {
    if (!isHyperfocus) {
      // Clear dimming
      setNodes(nds => nds.map(n => ({
        ...n,
        className: (n.className || '').replace(' dimmed', '')
      })));
      return;
    }

    const focusSet = getFocusSet(selectedNodeId);

    setNodes(nds => nds.map(n => {
      const isDimmed = selectedNodeId && !focusSet.has(n.id);
      let newClass = (n.className || '').replace(' dimmed', '');
      if (isDimmed) newClass += ' dimmed';

      // Only update if changed
      if (newClass !== n.className) {
        return { ...n, className: newClass };
      }
      return n;
    }));
  }, [isHyperfocus, selectedNodeId, edges, setNodes]);

  // Trigger update when relevant state changes
  // We need a useEffect that calls this
  useEffect(() => {
    updateNodeDimming();
  }, [isHyperfocus, selectedNodeId, updateNodeDimming]); // edges omitted to avoid loop on simple moves, but technically needed if graph changes


  return (
    <div style={{ width: '100vw', height: '100vh', background: '#2d3436' }} className={containerClass}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        onMove={handleMove}
        onSelectionChange={handleSelectionChange}
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        fitView
      >
        <Background color="#b2bec3" gap={20} />
        <Controls />
        <Panel position="top-right">
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            {/* Preset Selector */}
            <select
              onChange={(e) => {
                if (e.target.value === 'quantum') loadPreset(QUANTUM_PRESET);
                if (e.target.value === 'dogma') loadPreset(CENTRAL_DOGMA_PRESET);
                if (e.target.value === 'enzyme') loadPreset(RESTRICTION_ENZYME_PRESET);
              }}
              defaultValue="dogma"
              style={{
                padding: '10px',
                borderRadius: '5px',
                border: 'none',
                background: '#dfe6e9',
                color: '#2d3436',
                fontWeight: 'bold',
                cursor: 'pointer',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
              }}
            >
              <option value="dogma">🧬 Central Dogma Demo</option>
              <option value="enzyme">✂️ Restriction Enzyme Demo</option>
              <option value="quantum">⚛️ Quantum Circuit Demo</option>
            </select>

            {/* Hyperfocus Toggle */}
            <button
              onClick={() => setIsHyperfocus(!isHyperfocus)}
              style={{
                padding: '8px 12px',
                borderRadius: '5px',
                border: isHyperfocus ? '2px solid #74b9ff' : 'none',
                background: isHyperfocus ? '#0984e3' : '#dfe6e9',
                color: isHyperfocus ? 'white' : 'black',
                cursor: 'pointer',
                fontWeight: 'bold',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
              title="Toggle Hyperfocus Mode"
            >
              {isHyperfocus ? '🎯 Hyperfocus ON' : '👁️ Focus'}
            </button>

            <div style={{ width: '1px', height: '24px', background: '#b2bec3', margin: '0 10px' }}></div>

            <button
              onClick={handleExport}
              style={{
                padding: '10px 20px',
                background: '#6c5ce7',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                fontWeight: 'bold',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
              }}
            >
              ⚛️ Export Qiskit
            </button>
            <button
              onClick={handleBioExport}
              style={{
                padding: '10px 20px',
                background: '#00b894',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                fontWeight: 'bold',
                boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
              }}
            >
              🧬 Export BioPython
            </button>
          </div>
        </Panel>
      </ReactFlow>

      <ExportModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        code={exportCode}
      />
    </div>
  );
}

export default App;

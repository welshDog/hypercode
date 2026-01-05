# VIS5: Cloud Sync — Save/Load MVP Implementation

## Objective
Add **Save/Load Flow** persistence to HyperFlow.  
MVP scope: **Local JSON export/import only** (cloud layer abstracted for future).

---

## Why This Matters

Right now, if you close the browser tab, your flow is gone. This playbook:
- ✅ Lets you **Save flow as `.json` file** locally
- ✅ **Load flow from JSON** back into editor  
- ✅ Sets up **abstraction layer** so swapping to cloud storage (Firebase, Supabase, etc.) is trivial
- ✅ Keeps React Flow graph structure 100% portable

---

## Phase 1: Storage Abstraction Layer (10 min)

### 1.1 Create Storage Interface

**Location:** `hyperflow-editor/src/storage/StorageProvider.ts` (new)

```typescript
/**
 * Abstract storage interface.
 * Allows swapping between localStorage, IndexedDB, cloud APIs, etc.
 */

export interface FlowMetadata {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
  tags?: string[];
}

export interface SavedFlow extends FlowMetadata {
  nodes: any[]; // React Flow nodes
  edges: any[]; // React Flow edges
}

export interface IStorageProvider {
  /**
   * Save a flow.
   */
  save(flow: SavedFlow): Promise<void>;

  /**
   * Load a flow by ID.
   */
  load(id: string): Promise<SavedFlow | null>;

  /**
   * List all saved flows.
   */
  listFlows(): Promise<FlowMetadata[]>;

  /**
   * Delete a flow.
   */
  delete(id: string): Promise<void>;

  /**
   * Export flow as JSON string (for download).
   */
  exportJSON(flow: SavedFlow): string;

  /**
   * Import flow from JSON string (from file upload).
   */
  importJSON(jsonString: string): SavedFlow;
}
```

### 1.2 Local JSON Storage Implementation

**Location:** `hyperflow-editor/src/storage/LocalStorageProvider.ts` (new)

```typescript
import { IStorageProvider, SavedFlow, FlowMetadata } from './StorageProvider';

/**
 * MVP: Store flows in browser localStorage + allow JSON file export/import.
 * Later: swap for cloud storage without changing consumer code.
 */
export class LocalStorageProvider implements IStorageProvider {
  private readonly STORAGE_KEY = 'hyperflow_flows';
  private readonly MAX_STORAGE = 5 * 1024 * 1024; // 5MB limit

  async save(flow: SavedFlow): Promise<void> {
    const flows = this.loadAllFlows();
    const index = flows.findIndex((f) => f.id === flow.id);

    if (index >= 0) {
      flows[index] = flow;
    } else {
      flows.push(flow);
    }

    // Check storage size
    const serialized = JSON.stringify(flows);
    if (serialized.length > this.MAX_STORAGE) {
      throw new Error(
        `Flow storage exceeds ${this.MAX_STORAGE} bytes. Delete old flows.`
      );
    }

    localStorage.setItem(this.STORAGE_KEY, serialized);
  }

  async load(id: string): Promise<SavedFlow | null> {
    const flows = this.loadAllFlows();
    return flows.find((f) => f.id === id) || null;
  }

  async listFlows(): Promise<FlowMetadata[]> {
    return this.loadAllFlows().map((f) => ({
      id: f.id,
      name: f.name,
      description: f.description,
      createdAt: f.createdAt,
      updatedAt: f.updatedAt,
      tags: f.tags,
    }));
  }

  async delete(id: string): Promise<void> {
    const flows = this.loadAllFlows().filter((f) => f.id !== id);
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(flows));
  }

  exportJSON(flow: SavedFlow): string {
    return JSON.stringify(flow, null, 2);
  }

  importJSON(jsonString: string): SavedFlow {
    try {
      const flow = JSON.parse(jsonString) as SavedFlow;
      // Validate required fields
      if (!flow.id || !flow.name || !flow.nodes || !flow.edges) {
        throw new Error('Invalid flow format: missing required fields.');
      }
      return flow;
    } catch (error) {
      throw new Error(`Failed to import flow: ${error}`);
    }
  }

  private loadAllFlows(): SavedFlow[] {
    const raw = localStorage.getItem(this.STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  }
}
```

---

## Phase 2: React Hooks for Save/Load (15 min)

### 2.1 Create useFlowPersistence Hook

**Location:** `hyperflow-editor/src/hooks/useFlowPersistence.ts` (new)

```typescript
import { useCallback, useState } from 'react';
import { Node, Edge } from 'reactflow';
import { IStorageProvider, SavedFlow, FlowMetadata } from '../storage/StorageProvider';

interface UseFlowPersistenceOptions {
  storageProvider: IStorageProvider;
  currentFlowId: string;
  currentFlowName: string;
}

export function useFlowPersistence({
  storageProvider,
  currentFlowId,
  currentFlowName,
}: UseFlowPersistenceOptions) {
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [savedFlows, setSavedFlows] = useState<FlowMetadata[]>([]);

  /**
   * Save current flow.
   */
  const saveFlow = useCallback(
    async (nodes: Node[], edges: Edge[], description?: string) => {
      setIsSaving(true);
      setError(null);
      try {
        const flow: SavedFlow = {
          id: currentFlowId,
          name: currentFlowName,
          description,
          nodes,
          edges,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        };
        await storageProvider.save(flow);
      } catch (err) {
        setError(`Failed to save: ${err}`);
      } finally {
        setIsSaving(false);
      }
    },
    [storageProvider, currentFlowId, currentFlowName]
  );

  /**
   * Load a flow by ID.
   */
  const loadFlow = useCallback(
    async (id: string): Promise<SavedFlow | null> => {
      setIsLoading(true);
      setError(null);
      try {
        const flow = await storageProvider.load(id);
        return flow;
      } catch (err) {
        setError(`Failed to load: ${err}`);
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [storageProvider]
  );

  /**
   * List all saved flows.
   */
  const refreshFlowList = useCallback(async () => {
    try {
      const flows = await storageProvider.listFlows();
      setSavedFlows(flows);
    } catch (err) {
      setError(`Failed to list flows: ${err}`);
    }
  }, [storageProvider]);

  /**
   * Delete a flow.
   */
  const deleteFlow = useCallback(
    async (id: string) => {
      try {
        await storageProvider.delete(id);
        setSavedFlows((prev) => prev.filter((f) => f.id !== id));
      } catch (err) {
        setError(`Failed to delete: ${err}`);
      }
    },
    [storageProvider]
  );

  /**
   * Download flow as JSON file.
   */
  const downloadFlowAsJSON = useCallback(
    async (id: string) => {
      try {
        const flow = await storageProvider.load(id);
        if (!flow) throw new Error('Flow not found');

        const json = storageProvider.exportJSON(flow);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${flow.name}.hyperflow.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } catch (err) {
        setError(`Failed to download: ${err}`);
      }
    },
    [storageProvider]
  );

  /**
   * Upload and import flow from JSON file.
   */
  const importFlowFromFile = useCallback(
    async (file: File): Promise<SavedFlow | null> => {
      try {
        const text = await file.text();
        const flow = storageProvider.importJSON(text);
        // Optionally save it
        await storageProvider.save(flow);
        return flow;
      } catch (err) {
        setError(`Failed to import: ${err}`);
        return null;
      }
    },
    [storageProvider]
  );

  return {
    saveFlow,
    loadFlow,
    refreshFlowList,
    deleteFlow,
    downloadFlowAsJSON,
    importFlowFromFile,
    savedFlows,
    isSaving,
    isLoading,
    error,
  };
}
```

---

## Phase 3: UI Components (20 min)

### 3.1 Save/Load Toolbar

**Location:** `hyperflow-editor/src/components/SaveLoadToolbar.tsx` (new)

```typescript
import React, { useEffect, useRef } from 'react';
import { SavedFlow } from '../storage/StorageProvider';

interface SaveLoadToolbarProps {
  onSave: (description?: string) => Promise<void>;
  onLoadClick: () => void;
  onDownload: () => Promise<void>;
  onImportFile: (file: File) => Promise<void>;
  isSaving: boolean;
  isLoading: boolean;
  error: string | null;
  savedFlows: any[];
  currentFlowName: string;
}

export function SaveLoadToolbar({
  onSave,
  onLoadClick,
  onDownload,
  onImportFile,
  isSaving,
  isLoading,
  error,
  savedFlows,
  currentFlowName,
}: SaveLoadToolbarProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSaveClick = () => {
    onSave(`Saved at ${new Date().toLocaleTimeString()}`);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImportFile(file);
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        gap: '8px',
        padding: '8px 12px',
        backgroundColor: '#f5f5f5',
        borderBottom: '1px solid #ddd',
        alignItems: 'center',
        flexWrap: 'wrap',
      }}
    >
      {/* Current Flow Name */}
      <span style={{ fontSize: '12px', fontWeight: 'bold' }}>
        📄 {currentFlowName}
      </span>

      {/* Save Button */}
      <button
        onClick={handleSaveClick}
        disabled={isSaving}
        style={{
          padding: '6px 12px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px',
          opacity: isSaving ? 0.6 : 1,
        }}
      >
        {isSaving ? '💾 Saving...' : '💾 Save Flow'}
      </button>

      {/* Download Button */}
      <button
        onClick={onDownload}
        style={{
          padding: '6px 12px',
          backgroundColor: '#2196F3',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px',
        }}
      >
        ⬇️ Download JSON
      </button>

      {/* Import Button */}
      <div>
        <input
          ref={fileInputRef}
          type="file"
          accept=".json,.hyperflow.json"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        <button
          onClick={() => fileInputRef.current?.click()}
          style={{
            padding: '6px 12px',
            backgroundColor: '#FF9800',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '12px',
          }}
        >
          ⬆️ Import JSON
        </button>
      </div>

      {/* Load Button */}
      <button
        onClick={onLoadClick}
        disabled={isLoading || savedFlows.length === 0}
        style={{
          padding: '6px 12px',
          backgroundColor: '#9C27B0',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '12px',
          opacity: isLoading ? 0.6 : 1,
        }}
      >
        {isLoading ? '⏳ Loading...' : '📂 Open Flow'}
      </button>

      {/* Error Message */}
      {error && (
        <span style={{ fontSize: '11px', color: 'red', marginLeft: 'auto' }}>
          ⚠️ {error}
        </span>
      )}
    </div>
  );
}
```

### 3.2 Flow Selector Modal

**Location:** `hyperflow-editor/src/components/FlowSelectorModal.tsx` (new)

```typescript
import React from 'react';
import { FlowMetadata } from '../storage/StorageProvider';

interface FlowSelectorModalProps {
  flows: FlowMetadata[];
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
  onClose: () => void;
}

export function FlowSelectorModal({
  flows,
  onSelect,
  onDelete,
  onClose,
}: FlowSelectorModalProps) {
  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0,0,0,0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      onClick={onClose}
    >
      <div
        style={{
          backgroundColor: 'white',
          borderRadius: '8px',
          padding: '24px',
          maxWidth: '500px',
          maxHeight: '70vh',
          overflowY: 'auto',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 style={{ margin: '0 0 16px 0' }}>📂 Open Saved Flow</h2>

        {flows.length === 0 ? (
          <p style={{ color: '#999' }}>No saved flows yet.</p>
        ) : (
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {flows.map((flow) => (
              <li
                key={flow.id}
                style={{
                  padding: '12px',
                  borderBottom: '1px solid #eee',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div onClick={() => onSelect(flow.id)} style={{ cursor: 'pointer', flex: 1 }}>
                  <strong>{flow.name}</strong>
                  <p style={{ fontSize: '12px', color: '#999', margin: '4px 0 0 0' }}>
                    Updated: {new Date(flow.updatedAt).toLocaleString()}
                  </p>
                </div>
                <button
                  onClick={() => onDelete(flow.id)}
                  style={{
                    padding: '4px 8px',
                    backgroundColor: '#f44336',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: '11px',
                  }}
                >
                  Delete
                </button>
              </li>
            ))}
          </ul>
        )}

        <button
          onClick={onClose}
          style={{
            marginTop: '16px',
            padding: '8px 16px',
            backgroundColor: '#ccc',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Close
        </button>
      </div>
    </div>
  );
}
```

---

## Phase 4: Integration into Main Editor (10 min)

### 4.1 Wire into HyperFlow Main Component

**Location:** `hyperflow-editor/src/App.tsx` or main editor component (update existing)

```typescript
import { useState, useCallback, useEffect } from 'react';
import { LocalStorageProvider } from './storage/LocalStorageProvider';
import { useFlowPersistence } from './hooks/useFlowPersistence';
import { SaveLoadToolbar } from './components/SaveLoadToolbar';
import { FlowSelectorModal } from './components/FlowSelectorModal';

export function HyperFlowEditor() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [currentFlowId, setCurrentFlowId] = useState(() => 
    `flow_${Date.now()}`
  );
  const [currentFlowName, setCurrentFlowName] = useState('Untitled Flow');
  const [showFlowSelector, setShowFlowSelector] = useState(false);

  const storageProvider = new LocalStorageProvider();
  const {
    saveFlow,
    loadFlow,
    refreshFlowList,
    deleteFlow,
    downloadFlowAsJSON,
    importFlowFromFile,
    savedFlows,
    isSaving,
    isLoading,
    error,
  } = useFlowPersistence({
    storageProvider,
    currentFlowId,
    currentFlowName,
  });

  // Load flow list on mount
  useEffect(() => {
    refreshFlowList();
  }, [refreshFlowList]);

  const handleSave = useCallback(() => {
    saveFlow(nodes, edges);
  }, [saveFlow, nodes, edges]);

  const handleLoadClick = () => {
    setShowFlowSelector(true);
  };

  const handleSelectFlow = useCallback(
    async (id: string) => {
      const flow = await loadFlow(id);
      if (flow) {
        setCurrentFlowId(flow.id);
        setCurrentFlowName(flow.name);
        setNodes(flow.nodes);
        setEdges(flow.edges);
        setShowFlowSelector(false);
      }
    },
    [loadFlow]
  );

  const handleImportFile = useCallback(
    async (file: File) => {
      const flow = await importFlowFromFile(file);
      if (flow) {
        setCurrentFlowId(flow.id);
        setCurrentFlowName(flow.name);
        setNodes(flow.nodes);
        setEdges(flow.edges);
        await refreshFlowList();
      }
    },
    [importFlowFromFile, refreshFlowList]
  );

  return (
    <>
      <SaveLoadToolbar
        onSave={handleSave}
        onLoadClick={handleLoadClick}
        onDownload={() => downloadFlowAsJSON(currentFlowId)}
        onImportFile={handleImportFile}
        isSaving={isSaving}
        isLoading={isLoading}
        error={error}
        savedFlows={savedFlows}
        currentFlowName={currentFlowName}
      />

      {showFlowSelector && (
        <FlowSelectorModal
          flows={savedFlows}
          onSelect={handleSelectFlow}
          onDelete={deleteFlow}
          onClose={() => setShowFlowSelector(false)}
        />
      )}

      {/* Rest of your ReactFlow canvas... */}
    </>
  );
}
```

---

## Phase 5: Update README (5 min)

Add to README under "HyperFlow: The Visual Cockpit" section:

```markdown
### Cloud Sync (VIS5)

**Now MVP:** Save and load flows locally with one click.

- **💾 Save Flow** → Browser localStorage
- **⬇️ Download** → JSON file to your machine
- **⬆️ Import** → Load from JSON file
- **📂 Open Flow** → Browse + load previously saved flows

**Coming Soon:** Cloud sync (Firebase, Supabase) via the same interface — no UI changes needed.

```
Save → Close browser → Come back → Load = instant recovery.
```
```

---

## Phase 6: Testing Checklist (10 min)

### 6.1 Manual Test Plan

- [ ] Create a flow with 3+ nodes + edges
- [ ] Click **"💾 Save Flow"** → no errors
- [ ] Close the browser tab completely
- [ ] Reopen HyperFlow → flow data gone (fresh start)
- [ ] Click **"📂 Open Flow"** → modal appears with saved flow
- [ ] Select saved flow → nodes/edges restore correctly
- [ ] Click **"⬇️ Download JSON"** → file downloads as `flowname.hyperflow.json`
- [ ] Click **"⬆️ Import JSON"** → select downloaded file
- [ ] Verify flow loads from imported file
- [ ] Delete a flow from modal → verify it's gone from list
- [ ] Test error case: import corrupted JSON → error message displays

---

## Expected Time: ~70 minutes total

| Step | Time |
|------|------|
| 1. Storage Abstraction | 10 min |
| 2. React Hooks | 15 min |
| 3. UI Components | 20 min |
| 4. Integration | 10 min |
| 5. README | 5 min |
| 6. Testing | 10 min |
| **TOTAL** | **~70 min** |

---

## Why This Architecture Is Future-Proof

1. **`IStorageProvider` interface** = swap storage backend without touching UI
2. **All serialization in one place** = easy JSON schema versioning later
3. **No cloud vendor lock-in** = implement Firebase/Supabase later as new `StorageProvider`
4. **Portable flows** = users can move flows between machines via JSON export

### Future: Cloud Storage Implementation (Not Needed Yet)

When you're ready, create `CloudStorageProvider.ts`:

```typescript
export class CloudStorageProvider implements IStorageProvider {
  constructor(private firebaseApp: Firebase) {}
  
  async save(flow: SavedFlow): Promise<void> {
    // Firestore: db.collection('flows').doc(flow.id).set(flow)
  }
  
  async load(id: string): Promise<SavedFlow | null> {
    // Firestore: db.collection('flows').doc(id).get()
  }
  
  // ... rest of interface
}
```

Then swap `new LocalStorageProvider()` → `new CloudStorageProvider(firebaseApp)` in App.tsx. Done.

---

## Quick Questions?

1. **Do you use TypeScript or JavaScript in HyperFlow?** (I wrote TS; can convert to JS)
2. **Is your main component already using React hooks state?** (Need to know for integration)
3. **Want localStorage limit warnings, or silent overflow?**

Ready to smash this out? 🚀

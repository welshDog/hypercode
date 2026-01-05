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
  viewport?: { x: number; y: number; zoom: number };
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

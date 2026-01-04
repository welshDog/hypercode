import type { IStorageProvider, SavedFlow, FlowMetadata } from './StorageProvider';

/**
 * MVP: Store flows in browser localStorage + allow JSON file export/import.
 * Later: swap for cloud storage without changing consumer code.
 */
export class LocalStorageProvider implements IStorageProvider {
  private readonly STORAGE_KEY = 'hyperflow_flows';
  
  // Helper to get all flows from localStorage
  private loadAllFlows(): SavedFlow[] {
    try {
      const json = localStorage.getItem(this.STORAGE_KEY);
      return json ? JSON.parse(json) : [];
    } catch (e) {
      console.error('Failed to load flows from localStorage', e);
      return [];
    }
  }

  // Helper to save all flows to localStorage
  private saveAllFlows(flows: SavedFlow[]): void {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(flows));
    } catch (e) {
      console.error('Failed to save flows to localStorage - quota exceeded?', e);
      throw new Error('Storage quota exceeded');
    }
  }

  async save(flow: SavedFlow): Promise<void> {
    const flows = this.loadAllFlows();
    const index = flows.findIndex((f) => f.id === flow.id);

    if (index >= 0) {
      flows[index] = { ...flow, updatedAt: new Date().toISOString() };
    } else {
      flows.push({ ...flow, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
    }

    this.saveAllFlows(flows);
  }

  async load(id: string): Promise<SavedFlow | null> {
    const flows = this.loadAllFlows();
    return flows.find((f) => f.id === id) || null;
  }

  async listFlows(): Promise<FlowMetadata[]> {
    const flows = this.loadAllFlows();
    // Return lightweight metadata only
    return flows.map(({ id, name, description, createdAt, updatedAt, tags }) => ({
      id,
      name,
      description,
      createdAt,
      updatedAt,
      tags
    }));
  }

  async delete(id: string): Promise<void> {
    let flows = this.loadAllFlows();
    flows = flows.filter(f => f.id !== id);
    this.saveAllFlows(flows);
  }

  exportJSON(flow: SavedFlow): string {
    return JSON.stringify(flow, null, 2);
  }

  importJSON(jsonString: string): SavedFlow {
    try {
      const flow = JSON.parse(jsonString);
      // Basic validation
      if (!flow.nodes || !flow.edges) {
        throw new Error('Invalid flow file: missing nodes or edges');
      }
      return flow as SavedFlow;
    } catch (e) {
      throw new Error('Invalid JSON file');
    }
  }
}

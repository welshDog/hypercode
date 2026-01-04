import type { IStorageProvider, SavedFlow, FlowMetadata } from './StorageProvider';

/**
 * SIMULATED Cloud Storage Provider.
 * Mimics network latency and async operations.
 * Stores data in localStorage with a 'cloud_' prefix to simulate a remote DB.
 */
export class MockCloudStorageProvider implements IStorageProvider {
  private readonly CLOUD_DELAY_MS = 800; // Simulate network latency
  private readonly FAILURE_RATE = 0.0; // 0% failure for now, can increase for testing error states
  private readonly STORAGE_KEY = 'cloud_hyperflow_flows';

  private async delay(): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, this.CLOUD_DELAY_MS));
  }

  private simulateNetworkCondition(): void {
    if (Math.random() < this.FAILURE_RATE) {
      throw new Error('Network Error: Connection timed out');
    }
  }

  // Helper to get all flows from "Cloud"
  private getCloudStore(): SavedFlow[] {
    try {
      const json = localStorage.getItem(this.STORAGE_KEY);
      return json ? JSON.parse(json) : [];
    } catch (e) {
      console.error('Cloud store corrupted', e);
      return [];
    }
  }

  // Helper to save to "Cloud"
  private setCloudStore(flows: SavedFlow[]): void {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(flows));
  }

  async save(flow: SavedFlow): Promise<void> {
    await this.delay();
    this.simulateNetworkCondition();

    const flows = this.getCloudStore();
    const index = flows.findIndex((f) => f.id === flow.id);

    // Update or Insert
    if (index >= 0) {
      flows[index] = { ...flow, updatedAt: new Date().toISOString() };
    } else {
      flows.push({ ...flow, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() });
    }

    this.setCloudStore(flows);
    console.log('[Cloud] Saved flow:', flow.id);
  }

  async load(id: string): Promise<SavedFlow | null> {
    await this.delay();
    this.simulateNetworkCondition();

    const flows = this.getCloudStore();
    return flows.find((f) => f.id === id) || null;
  }

  async listFlows(): Promise<FlowMetadata[]> {
    await this.delay();
    this.simulateNetworkCondition();

    const flows = this.getCloudStore();
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
    await this.delay();
    this.simulateNetworkCondition();

    let flows = this.getCloudStore();
    flows = flows.filter(f => f.id !== id);
    this.setCloudStore(flows);
  }

  exportJSON(flow: SavedFlow): string {
    return JSON.stringify(flow, null, 2);
  }

  importJSON(jsonString: string): SavedFlow {
    try {
      const flow = JSON.parse(jsonString);
      if (!flow.nodes || !flow.edges) {
        throw new Error('Invalid flow file: missing nodes or edges');
      }
      return flow as SavedFlow;
    } catch (e) {
      throw new Error('Invalid JSON file');
    }
  }
}

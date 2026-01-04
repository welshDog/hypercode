import { SupabaseClient } from '@supabase/supabase-js';
import type { IStorageProvider, SavedFlow, FlowMetadata } from './StorageProvider';

export class SupabaseStorageProvider implements IStorageProvider {
  private client: SupabaseClient;
  private readonly TABLE_NAME = 'flows';

  constructor(client: SupabaseClient) {
    this.client = client;
  }

  async save(flow: SavedFlow): Promise<void> {
    const { data: { user } } = await this.client.auth.getUser();
    if (!user) {
      console.warn('User not authenticated, skipping save.');
      return;
    }

    const { error } = await this.client
      .from(this.TABLE_NAME)
      .upsert({
        id: flow.id,
        owner_id: user.id,
        name: flow.name,
        description: flow.description,
        nodes: flow.nodes,
        edges: flow.edges,
        viewport: flow.viewport,
        tags: flow.tags || [],
        // created_at handled by DB default for new rows
        // updated_at handled by DB trigger
      });

    if (error) {
      console.error('Supabase save error:', error);
      throw new Error(`Failed to save flow: ${error.message}`);
    }
  }

  async load(id: string): Promise<SavedFlow | null> {
    const { data, error } = await this.client
      .from(this.TABLE_NAME)
      .select('*')
      .eq('id', id)
      .single();

    if (error) {
      // If code is PGRST116, it means no rows returned (not found)
      if (error.code === 'PGRST116') return null;
      console.error('Supabase load error:', error);
      throw new Error(`Failed to load flow: ${error.message}`);
    }

    if (!data) return null;

    return {
      id: data.id,
      name: data.name,
      description: data.description,
      createdAt: data.created_at,
      updatedAt: data.updated_at,
      nodes: data.nodes,
      edges: data.edges,
      viewport: data.viewport,
      tags: data.tags,
    } as SavedFlow;
  }

  async listFlows(): Promise<FlowMetadata[]> {
    const { data, error } = await this.client
      .from(this.TABLE_NAME)
      .select('id, name, description, created_at, updated_at, tags')
      .order('updated_at', { ascending: false });

    if (error) {
      console.error('Supabase list error:', error);
      throw new Error(`Failed to list flows: ${error.message}`);
    }

    return (data || []).map((row: any) => ({
      id: row.id,
      name: row.name,
      description: row.description,
      createdAt: row.created_at,
      updatedAt: row.updated_at,
      tags: row.tags,
    }));
  }

  async delete(id: string): Promise<void> {
    const { error } = await this.client
      .from(this.TABLE_NAME)
      .delete()
      .eq('id', id);

    if (error) {
      console.error('Supabase delete error:', error);
      throw new Error(`Failed to delete flow: ${error.message}`);
    }
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
      throw new Error('Invalid JSON string');
    }
  }
}

# ⚡ Supabase Cloud Sync Setup

Enable real-time cloud persistence for your HyperFlow Editor.

## 1. Create a Supabase Project
1. Go to [database.new](https://database.new) and create a new project.
2. Wait for the database to provision.

## 2. Get API Keys
1. Go to **Project Settings** -> **API**.
2. Copy the **Project URL** and **anon public** key.
3. Rename `.env.example` to `.env` in the `hyperflow-editor` root.
4. Paste your keys:
   ```env
   VITE_SUPABASE_URL=https://your-project.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

## 3. Run Production SQL
Go to the **SQL Editor** in your Supabase dashboard and run this script to create the production-ready schema with RLS, triggers, and indexes:

```sql
-- ⚡ HyperFlow Production-Ready Schema

-- 1. Create table with smart defaults and owner_id
CREATE TABLE IF NOT EXISTS public.flows (
  id text PRIMARY KEY,
  owner_id uuid NOT NULL default auth.uid(), -- 🔒 Security: each flow has an owner
  name text,
  description text,
  nodes jsonb NOT NULL DEFAULT '[]'::jsonb,
  edges jsonb NOT NULL DEFAULT '[]'::jsonb,
  viewport jsonb NOT NULL DEFAULT '{}'::jsonb,
  tags text[] NOT NULL DEFAULT ARRAY[]::text[],
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now()
);

-- 2. Auto-update timestamp trigger (No more manual dates!)
CREATE OR REPLACE FUNCTION public.flows_updated_at()
RETURNS trigger AS $$
BEGIN
  NEW.updated_at := now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
BEFORE UPDATE ON public.flows
FOR EACH ROW
EXECUTE FUNCTION flows_updated_at();

-- 3. Performance indexes (Speed at scale)
CREATE INDEX IF NOT EXISTS idx_flows_owner ON public.flows (owner_id);
CREATE INDEX IF NOT EXISTS idx_flows_created ON public.flows (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_flows_tags ON public.flows USING GIN (tags);

-- 4. Security policies (RLS Enabled)
ALTER TABLE public.flows ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users manage own flows"
ON public.flows
FOR ALL
TO authenticated
USING (owner_id = auth.uid())
WITH CHECK (owner_id = auth.uid());
```

## 4. Verify & Authenticate
**Important:** This schema enforces authentication.
1.  **Create a User:** Go to **Authentication** in Supabase and add a user (or use the magic link feature).
2.  **Login in App:** Since the current UI doesn't have a login screen yet, you can temporarily hardcode a login in `App.tsx` or use the Supabase JS client in the console to sign in:
    ```js
    await supabase.auth.signInWithPassword({ email: '...', password: '...' })
    ```
3.  **Restart:**
    ```bash
    npm run dev
    ```
4.  Check the browser console. You should see `Using Supabase Cloud Storage`.

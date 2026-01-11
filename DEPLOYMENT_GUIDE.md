# 🚀 Deployment Guide: BROski Bot & Dashboard

You are deploying the **HyperCode Stack**:
1. **Backend**: Discord Bot + Express API (Node.js)
2. **Frontend**: React Dashboard (Vite Static Site)

---

## 🏗️ Option 1: The "Easy" Way (Render.com)
We recommend **Render** because it supports both Background Workers (Bot) and Static Sites (Dashboard) easily.

### Part A: Deploy the Backend (Bot + API)
1. Push your code to GitHub.
2. Go to [dashboard.render.com](https://dashboard.render.com) -> New -> **Web Service**.
3. Connect your GitHub repo.
4. **Settings**:
   - **Root Directory**: `tools/discord-bot`
   - **Build Command**: `npm install`
   - **Start Command**: `node src/index.js`
5. **Environment Variables**:
   - `DISCORD_TOKEN`: (Your Token)
   - `DISCORD_CLIENT_ID`: (Your ID)
   - `DISCORD_CLIENT_SECRET`: (Your Secret)
   - `MONGODB_URI`: (Your Atlas Connection String)
   - `OPENAI_API_KEY`: (Optional)
   - `FRONTEND_URL`: `https://your-dashboard-name.onrender.com` (Add this AFTER you deploy the frontend)
6. Click **Deploy**.

### Part B: Deploy the Frontend (Dashboard)
1. Go to Render Dashboard -> New -> **Static Site**.
2. Connect the same GitHub repo.
3. **Settings**:
   - **Root Directory**: `web/dashboard`
   - **Build Command**: `npm run build`
   - **Publish Directory**: `dist`
4. **Environment Variables**:
   - `VITE_API_URL`: Copy the URL from Part A (e.g., `https://broski-bot.onrender.com`) - **Do not add a trailing slash**.
5. Click **Deploy**.

### Part C: Link Them
1. Go back to your **Backend** service settings.
2. Update `FRONTEND_URL` to match your new **Frontend** URL.
3. Go to Discord Developer Portal -> OAuth2.
4. Add your Frontend URL (e.g., `https://hypercode-dash.onrender.com/auth/callback`) to the **Redirects**.
5. Update `DISCORD_REDIRECT_URI` in your Backend env vars if you set that explicitly.

---

## 🛠️ Option 2: The "Hacker" Way (VPS/Railway/Heroku)

### Backend
- Ensure you run `npm start` in `tools/discord-bot`.
- It exposes port `3000` (or `$PORT`).

### Frontend
- Run `npm run build` in `web/dashboard`.
- Serve the `dist` folder using Nginx, Apache, or `serve -s dist`.

---

## 🧪 Verify Deployment
1. Open your Dashboard URL.
2. Click **Login**.
3. It should redirect to Discord, then back to your Dashboard.
4. If you see "Welcome back, Commander" and real stats -> **SUCCESS**.

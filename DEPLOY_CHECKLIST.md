# 🚀 DEPLOYMENT CHECKLIST
**Mission:** Launch The HyperCode Agency to Production.

## 1. 🔑 Environment Variables (Render Dashboard)
When you create the Blueprint in Render, you will be asked for these values. Have them ready!

### Service: `hypercode-bot`
| Variable | Value / Notes |
| :--- | :--- |
| `DISCORD_TOKEN` | Your Bot Token from Discord Developer Portal. |
| `MONGODB_URI` | Your MongoDB Atlas Connection String. |
| `DISCORD_CLIENT_ID` | Your Application ID. |
| `NODE_VERSION` | `18.17.0` (Already set in yaml) |

### Service: `hypercode-dashboard`
| Variable | Value / Notes |
| :--- | :--- |
| `VITE_API_URL` | The URL of your `hypercode-bot` service (e.g., `https://hypercode-bot.onrender.com`). *Note: You might need to deploy the bot first to get this URL, or Render might predict it.* |

---

## 2. 📡 Deployment Steps
1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "feat: HyperCode Launch Ready"
   git push origin main
   ```
2. **Open Render**: Go to [dashboard.render.com](https://dashboard.render.com).
3. **New Blueprint**: Click **New +** -> **Blueprint**.
4. **Connect Repo**: Select your `THE HYPERCODE` repo.
5. **Review**: Render will detect `render.yaml`.
6. **Input Secrets**: Fill in the Env Vars from Step 1.
7. **Apply**: Click **Apply Changes**.

## 3. 🚦 Validation
- **Discord**: Type `/shop browse`. If it replies, we are live.
- **Dashboard**: Visit the provided URL. Check if the "Coach" widget loads.

*Good luck, Commander.* 🫡

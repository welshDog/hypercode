# 📘 Contributing to HyperCode

Welcome to the Agency. This document is the "Source of Truth" for how we build.

## 🛠️ Development Setup

### Prerequisites
- Node.js v16+
- MongoDB (Local or Atlas)
- Discord Bot Token

### Quick Start
1. **Clone & Install**
   ```bash
   git clone <repo>
   cd tools/discord-bot && npm install
   cd ../../web/dashboard && npm install
   ```

2. **Environment Variables**
   - Copy `.env.example` to `.env` in `tools/discord-bot`.
   - Set `DISCORD_TOKEN` and `MONGODB_URI`.

3. **Run the Stack**
   - **Bot**: `cd tools/discord-bot && npm run dev`
   - **Dashboard**: `cd web/dashboard && npm run dev`

---

## 🧪 Testing (The Vanguard Protocol)
Before pushing code, you MUST run the test suite.

```bash
cd tools/discord-bot
npm test
```

If tests fail, do not merge.

---

## 🧩 Adding Features

### Adding a Discord Command
1. Create file in `src/commands/<name>.js`.
2. Use `SlashCommandBuilder`.
3. Implement `execute(interaction)`.
4. **Neuro-Tip**: Keep responses concise and use emojis.

### Adding a Dashboard Widget
1. Create component in `src/components/`.
2. Use `framer-motion` for entrance animations.
3. Ensure high contrast (WCAG AA).

---

## 📝 Style Guide (Neurodivergent-First)
- **Comments**: Explain *Why*, not just *What*.
- **Variable Names**: Descriptive > Short. `isDatabaseConnected` > `dbConn`.
- **Functions**: Small, single-purpose functions. Avoid "God Objects".

---

*Maintained by The Archivist*

# 🤖 BROski Discord Bot (Node.js Edition)

This is the official Node.js implementation of the BROski Discord Bot, designed for the HyperCode community.

## 🏗️ Architecture
- **Runtime**: Node.js 18+
- **Framework**: discord.js v14
- **Database**: MongoDB (Mongoose)
- **Caching**: Redis (Planned)

## 🚀 Deployment
For a complete step-by-step guide on how to deploy this bot to a live server (or your local machine), read [DEPLOYMENT.md](DEPLOYMENT.md).

Quick Start (Windows):
```bash
start.bat
```

## 📂 Structure
- `src/index.js`: Main entry point. Connects to Mongo and Discord.
- `src/commands/`: Slash command definitions.
  - `hyperfocus.js`: Core logic for starting/stopping sessions and calculating rewards.
- `src/models/`: Mongoose schemas.
  - `User.js`: Stores profile, balance, and stats.
  - `Session.js`: Logs individual focus sessions.

## 📝 Features (MVP)
- **/hyperfocus start [type]**: Starts a session.
- **/hyperfocus stop**: Ends session, calculates BROski$ rewards.
- **Auto-User Creation**: Automatically creates DB profile on first command.

## 🔗 Research Alignment
This codebase aligns with the "BROski Bot Consolidated Research" document, implementing the Phase 1 MVP requirements.

## 🗺️ Phase 2 Roadmap
Based on the Consolidated Research, the next phase focuses on AI and Blockchain integration:

- [x] **AI Coach Integration**: Connect `/coach` to GPT-4 for personalized productivity advice.
- [ ] **Blockchain Layer**: Deploy Solana smart contract for BROski$ token minting.
- [x] **Leaderboard System**: Implement Redis-backed real-time leaderboards (`/leaderboard`).
- [ ] **Web Dashboard**: Create a React frontend for users to view stats and manage wallets.

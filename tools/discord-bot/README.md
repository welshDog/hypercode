# 🤖 BROski Discord Bot (Node.js Edition)

This is the official Node.js implementation of the BROski Discord Bot, designed for the HyperCode community.

## 🏗️ Architecture
- **Runtime**: Node.js 18+
- **Framework**: discord.js v14
- **Database**: MongoDB (Mongoose)
- **Caching**: Redis (Planned)

## 🚀 Setup

1.  **Install Dependencies**:
    ```bash
    npm install
    ```

2.  **Configuration**:
    - Copy `.env.example` to `.env`
    - Fill in your `DISCORD_TOKEN`, `CLIENT_ID`, and `MONGODB_URI`.

3.  **Run Development**:
    ```bash
    npm run dev
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

# 🚀 Deployment Guide: BROski Bot v0.2.0

So you're ready to take this live? Let's go.
This guide assumes you are deploying to a local test server (your PC) or a VPS.

## 📋 Prerequisites
1. **Node.js 16+** (You already have this)
2. **MongoDB** (You need a database running)
   - *Local*: `mongodb://localhost:27017/broski-bot`
   - *Cloud*: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (Free Tier is perfect)

## 🔑 1. Credentials Setup
You need to create a `.env` file in this directory (`tools/discord-bot/`).
Copy `.env.example` and fill in the blanks:

```bash
cp .env.example .env
```

### Where to get the keys?
- **DISCORD_TOKEN**: Discord Developer Portal -> Bot -> Reset Token
- **CLIENT_ID**: Discord Developer Portal -> General Information -> Application ID
- **GUILD_ID**: Right-click your Test Server in Discord -> Copy ID (Turn on Developer Mode in Settings -> Advanced first!)
- **MONGODB_URI**: Connection string from Compass or Atlas.
- **OPENAI_API_KEY**: (Optional) From platform.openai.com. If you leave this blank, the bot runs in "Offline Mode" (Logic only, no AI).

## 🏃 2. Running the Bot
We've made it simple.

**Windows:**
Double-click `start.bat`
*OR*
Run in terminal:
```powershell
./start.bat
```

**Linux/Mac:**
```bash
npm start
```

## 🐛 3. Verification Checklist
Once the console says `✅ Successfully reloaded application (/) commands.` and `🤖 BROski Bot Online!`:

1. **Go to your Discord Server**.
2. Type `/` and see if `hyperfocus`, `coach`, and `leaderboard` appear.
3. Run `/coach status` -> Should say "No active session".
4. Run `/hyperfocus start 25` -> Should start a session.
5. **Check Console**: Ensure no red errors appear.

## 🔄 4. Updating
If you change code:
1. `Ctrl+C` to stop the bot.
2. Run `start.bat` again.
   - *Note*: Commands update instantly because we use `GUILD_ID`.

## 🆘 Troubleshooting
- **"Commands not showing up"**: Did you put the correct `GUILD_ID` in `.env`? Did you invite the bot with `applications.commands` scope?
- **"MongoDB Connection Error"**: Is your Mongo service running? (`net start MongoDB` on Windows)

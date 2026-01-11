# 🚀 BROski$ Bot - Setup & Deployment Guide

## ✅ Quick Start (15 minutes)

### Step 1: Get Your Discord Bot Token
1. Go to **Discord Developer Portal** → https://discord.com/developers/applications
2. Click **"New Application"** → Name it "BROski Bot"
3. Go to **"Bot"** tab → Click **"Add Bot"**
4. Under TOKEN, click **"Copy"** (save this!)
5. Go to **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Permissions: `Send Messages`, `Read Messages/View Channels`, `Use Application Commands`
   - Copy generated URL, paste in browser to invite bot to your server

### Step 2: Install Dependencies
```bash
# On Raspberry Pi, Linux, or Mac:
pip install discord.py==2.3.0

# Windows (if you have Python 3.9+):
pip install discord.py==2.3.0
```

### Step 3: Save Bot Code
1. Save the `broski_bot.py` file to a folder (e.g., `~/broski_bot/`)
2. In that folder, set your Discord token as an environment variable:

**Linux/Mac:**
```bash
export DISCORD_TOKEN='YOUR_TOKEN_HERE'
python3 broski_bot.py
```

**Windows (PowerShell):**
```powershell
$env:DISCORD_TOKEN = 'YOUR_TOKEN_HERE'
python broski_bot.py
```

**Windows (Command Prompt):**
```cmd
set DISCORD_TOKEN=YOUR_TOKEN_HERE
python broski_bot.py
```

### Step 4: Test Commands
In your Discord server, try:
```
/balance
/complete code 1.0
/leaderboard
/stats
```

---

## 📊 Commands Overview

| Command | What It Does |
|---------|---|
| `/balance` | Show your BROski$ balance, level, streak, tasks completed |
| `/complete <type> [quality]` | Earn tokens (code, doc, art, community) |
| `/leaderboard [sort]` | Top earners (balance/lifetime/streak) |
| `/stats` | Economy fairness metrics (Gini coefficient) |
| `/help_broski` | Show all commands |

---

## 🎯 How to Earn BROski$

### Task Types & Base Rewards
- **code**: 50 BROski$ (code commits, PRs, bug fixes)
- **doc**: 40 BROski$ (tutorials, guides, documentation)
- **art**: 40 BROski$ (designs, graphics, visual content)
- **community**: 30 BROski$ (Discord help, mentoring, support)

### Reward Multipliers
- **Quality (0.5-1.5x)**: Rate your work honestly
- **Streak (1.0-2.0x)**: Cap at 2x after 10 consecutive days
- **Task Bonus (1.1x)**: Extra for diverse task types

### Example Earnable in One Week

```
Day 1: /complete code 1.0       → 50 BROski$ (streak x1.0)
Day 2: /complete doc 1.0        → 44 BROski$ (doc bonus 1.1x, streak x1.2)
Day 3: /complete code 1.0       → 55 BROski$ (streak x1.3)
Day 4: /complete community 1.0  → 39 BROski$ (community bonus, streak x1.4)
Day 5: /complete art 1.0        → 49 BROski$ (art bonus, streak x1.5)
Day 6: Break (let's say you were busy)
Day 7: /complete code 0.8       → 44 BROski$ (comeback bonus, quality x0.8, streak x2.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: ~281 BROski$ in one week, 6/7 tasks (healthy!)
```

---

## 🐳 Anti-Whale Safeguards

The system **prevents concentration**:
- **Gini Coefficient**: Tracks fairness (< 0.30 = fair, > 0.50 = concentrated)
- **Auto-cap**: If any user hits 5% of total supply, excess goes to community pool
- **Monthly audits**: Fairness review every 30 days
- **Transparent logs**: All transactions visible (audit trail)

---

## 🧠 Neurodivergent Features Built In

✅ **ADHD:** Instant feedback, streak bonuses, variety rewards  
✅ **Autism:** Predictable formulas, clear rules, optional customization  
✅ **Dyslexia:** Audio descriptions optional, simple text, color-coded feedback  
✅ **AuDHD:** Combo of instant wins + structured checkpoints  

---

## 📈 Fairness Dashboard

Run `/stats` to see:
- Total BROski$ distributed
- Average earning per user
- **Fairness Index** (Gini coefficient)
  - 0.00 = perfect equality
  - 0.30 = fair (target)
  - 0.50+ = unequal (needs rebalancing)

---

## 🚀 Advanced: Self-Hosting on Raspberry Pi

### Why Raspberry Pi?
- $50 one-time hardware cost
- Runs 24/7 (consumes ~5W)
- Perfect for HyperCode Zone
- Local database, no cloud fees

### Setup on Pi
```bash
# SSH into your Pi
ssh pi@raspberrypi.local

# Install Python (usually pre-installed)
python3 --version

# Create bot directory
mkdir ~/broski_bot
cd ~/broski_bot

# Install dependencies
pip install discord.py==2.3.0

# Copy broski_bot.py here
# nano broski_bot.py (paste code)

# Set token and run
export DISCORD_TOKEN='YOUR_TOKEN'
python3 broski_bot.py
```

### Run Bot on Pi Startup
Create `/home/pi/broski_bot/run.sh`:
```bash
#!/bin/bash
export DISCORD_TOKEN='YOUR_TOKEN'
cd /home/pi/broski_bot
python3 broski_bot.py >> broski_bot.log 2>&1
```

Then add to crontab:
```bash
crontab -e
# Add: @reboot /home/pi/broski_bot/run.sh
```

Now bot runs automatically when Pi reboots! 🔄

---

## 💾 Database Files

The bot creates:
- `broski_economy.db` — SQLite database (all data stored here)
- Backup regularly: `cp broski_economy.db broski_economy.backup.db`

---

## 🔧 Troubleshooting

**Bot won't start?**
```
ERROR: Set DISCORD_TOKEN environment variable!
```
→ Make sure you set the token before running

**Commands not showing?**
→ Restart bot: `Ctrl+C`, then rerun

**Users see no balance?**
→ First run `/balance` creates account

**Leaderboard empty?**
→ Users need to run `/complete` first

---

## 📅 Migration to Real Crypto (Year 3)

If you decide to go crypto:
1. Take SQLite snapshot of all balances
2. Deploy ERC-20 token on Base chain (~$500)
3. Airdrop 1:1 to all users over 30 days
4. Keep Discord bot as UI for trading/staking (optional)

**No rush**. This stays off-chain as long as you want. 😉

---

## 🎯 Next Steps

1. ✅ Get Discord token
2. ✅ Install discord.py
3. ✅ Run bot in test server
4. ✅ Test `/complete` command
5. ✅ Invite to HyperCode Zone
6. ✅ Run `/stats` monthly to check fairness
7. ✅ Adjust multipliers if needed (2-3 month review)
8. ✅ Celebrate first 100 BROski$ earned! 🎉

---

## 🆘 Need Help?

- Discord.py docs: https://discordpy.readthedocs.io/
- SQLite docs: https://www.sqlite.org/
- Join Discord devs community for questions

---

**You've got this, BROski! Let's build a fair, fun, neurodivergent-inclusive economy together. ♾️**

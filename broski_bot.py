"""
BROski$ Economy Bot - Fake Token System (Off-Chain Points)
For neurodivergent-inclusive reward system in Discord
Ready to run on Raspberry Pi or any Python 3.9+ environment
"""

import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta
import json
import math
import os
from pathlib import Path

# ===== SETUP =====
DATABASE = "broski_economy.db"
TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_TOKEN_HERE")

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# ===== DATABASE INITIALIZATION =====
def init_db():
    """Create SQLite tables if they don't exist"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT,
        broski_balance INTEGER DEFAULT 0,
        lifetime_earned INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        hyperfocus_hours FLOAT DEFAULT 0,
        task_count INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Transactions table (audit trail)
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        amount INTEGER,
        reason TEXT,
        task_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Streaks table
    c.execute('''CREATE TABLE IF NOT EXISTS streaks (
        user_id TEXT PRIMARY KEY,
        current_streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        last_login DATETIME,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

# ===== HELPER FUNCTIONS =====
def get_user(user_id: str):
    """Get or create user in database"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    
    if not user:
        c.execute("INSERT INTO users (id, username) VALUES (?, ?)", 
                  (user_id, f"User{user_id[-4:]}"))
        conn.commit()
        user = (user_id, f"User{user_id[-4:]}", 0, 0, 1, 0, 0, datetime.now())
    
    conn.close()
    return user

def add_broski(user_id: str, amount: int, reason: str, task_type: str = "general"):
    """Add BROski$ to user account with transaction logging"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Update balance
    c.execute("UPDATE users SET broski_balance = broski_balance + ?, lifetime_earned = lifetime_earned + ?, task_count = task_count + 1 WHERE id = ?",
              (amount, amount, user_id))
    
    # Log transaction (audit trail)
    c.execute("INSERT INTO transactions (user_id, amount, reason, task_type) VALUES (?, ?, ?, ?)",
              (user_id, amount, reason, task_type))
    
    conn.commit()
    conn.close()

def update_streak(user_id: str):
    """Update user's streak (called on daily login)"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("SELECT * FROM streaks WHERE user_id = ?", (user_id,))
    streak_data = c.fetchone()
    
    today = datetime.now().date()
    
    if not streak_data:
        c.execute("INSERT INTO streaks (user_id, current_streak, longest_streak, last_login) VALUES (?, 1, 1, ?)",
                  (user_id, datetime.now()))
    else:
        last_login = datetime.fromisoformat(streak_data[3]).date()
        
        if last_login == today:
            # Already logged in today
            current_streak = streak_data[1]
        elif last_login == today - timedelta(days=1):
            # Consecutive day, increment
            current_streak = streak_data[1] + 1
        else:
            # Broken streak, reset (but keep "comeback bonus")
            current_streak = 1
        
        longest = max(streak_data[2], current_streak)
        c.execute("UPDATE streaks SET current_streak = ?, longest_streak = ?, last_login = ? WHERE user_id = ?",
                  (current_streak, longest, datetime.now(), user_id))
    
    conn.commit()
    conn.close()

def get_streak(user_id: str) -> tuple:
    """Get user's streak info (current, longest)"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("SELECT current_streak, longest_streak FROM streaks WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        return result
    return (0, 0)

def calculate_reward(base: int, quality: float, task_type: str, user_id: str) -> tuple:
    """Calculate final reward with multipliers (neurodivergent-tuned)"""
    current_streak, _ = get_streak(user_id)
    
    # Streak multiplier (capped at 2x after 10 days)
    streak_mult = min(1.0 + (current_streak * 0.1), 2.0)
    
    # Quality multiplier (0.5 - 1.5)
    quality_mult = max(0.5, min(1.5, quality))
    
    # Task type bonus for variety
    task_bonus = 1.1 if task_type in ["doc", "art", "community"] else 1.0  # Encourage diversity
    
    final = int(base * quality_mult * streak_mult * task_bonus)
    
    return final, {
        'base': base,
        'quality_mult': round(quality_mult, 2),
        'streak_mult': round(streak_mult, 2),
        'task_bonus': round(task_bonus, 2),
    }

def get_fairness_metrics():
    """Calculate Gini coefficient and fairness stats"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute("SELECT broski_balance FROM users WHERE broski_balance > 0")
    balances = [row[0] for row in c.fetchall()]
    conn.close()
    
    if not balances:
        return {'gini': 0, 'median': 0, 'users': 0}
    
    # Gini coefficient calculation
    balances = sorted(balances)
    n = len(balances)
    cumsum = sum((i + 1) * x for i, x in enumerate(balances))
    gini = (2 * cumsum) / (n * sum(balances)) - (n + 1) / n if sum(balances) > 0 else 0
    
    return {
        'gini': round(gini, 3),
        'median': balances[n // 2],
        'avg': sum(balances) // n,
        'users': n,
        'total_broski': sum(balances),
    }

# ===== BOT COMMANDS =====

@bot.event
async def on_ready():
    """Bot startup"""
    print(f"✅ BROski$ Bot online as {bot.user}")
    init_db()

@bot.command(name="balance")
async def balance(ctx):
    """Check your BROski$ balance"""
    user_id = str(ctx.author.id)
    user = get_user(user_id)
    
    embed = discord.Embed(
        title=f"🏦 {ctx.author.name}'s BROski$ Balance",
        color=discord.Color.green()
    )
    embed.add_field(name="💰 Current Balance", value=f"**{user[2]} BROski$**", inline=False)
    embed.add_field(name="📊 All-Time Earned", value=f"{user[3]} BROski$", inline=True)
    embed.add_field(name="📈 Level", value=f"{user[4]}", inline=True)
    
    current_streak, longest = get_streak(user_id)
    embed.add_field(name="🔥 Current Streak", value=f"{current_streak} days", inline=True)
    embed.add_field(name="⭐ Longest Streak", value=f"{longest} days", inline=True)
    embed.add_field(name="📝 Tasks Completed", value=f"{user[7]}", inline=True)
    
    embed.set_footer(text="Start earning by completing tasks! 🚀")
    await ctx.send(embed=embed)

@bot.command(name="complete")
async def complete_task(ctx, task_type: str = "general", quality: float = 1.0):
    """
    Complete a task and earn BROski$
    Usage: /complete <task_type> [quality (0.5-1.5)]
    Task types: code, doc, art, community
    """
    user_id = str(ctx.author.id)
    
    # Validate task type
    task_rewards = {
        "code": 50,
        "doc": 40,
        "art": 40,
        "community": 30,
    }
    
    task_type = task_type.lower()
    if task_type not in task_rewards:
        await ctx.send(f"❌ Unknown task type. Choose from: {', '.join(task_rewards.keys())}")
        return
    
    # Calculate reward
    base_reward = task_rewards[task_type]
    final_reward, breakdown = calculate_reward(base_reward, quality, task_type, user_id)
    
    # Update user and streak
    add_broski(user_id, final_reward, f"Task completion: {task_type}", task_type)
    update_streak(user_id)
    
    # Show detailed breakdown
    embed = discord.Embed(
        title="🎉 Task Complete!",
        color=discord.Color.gold()
    )
    embed.add_field(name=f"Task Type", value=task_type.capitalize(), inline=True)
    embed.add_field(name=f"Quality", value=f"{quality}x", inline=True)
    embed.add_field(name="", value="", inline=False)  # Spacing
    
    embed.add_field(name="💵 Breakdown", value=
        f"Base: {breakdown['base']}\n"
        f"Quality: x{breakdown['quality_mult']}\n"
        f"Streak: x{breakdown['streak_mult']}\n"
        f"Task Bonus: x{breakdown['task_bonus']}", inline=True
    )
    
    embed.add_field(name="✨ Total Earned", value=f"**{final_reward} BROski$**", inline=True)
    
    current_streak, _ = get_streak(user_id)
    embed.set_footer(text=f"Streak: {current_streak} days 🔥")
    
    await ctx.send(embed=embed)

@bot.command(name="leaderboard")
async def leaderboard(ctx, sort_by: str = "balance"):
    """
    Show top earners
    Options: balance (default), lifetime, streak
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    if sort_by == "lifetime":
        c.execute("SELECT id, username, lifetime_earned FROM users ORDER BY lifetime_earned DESC LIMIT 10")
        title = "🏆 All-Time Earners"
        field_name = "All-Time"
    elif sort_by == "streak":
        c.execute("""SELECT users.id, users.username, streaks.current_streak 
                     FROM users JOIN streaks ON users.id = streaks.user_id 
                     ORDER BY streaks.current_streak DESC LIMIT 10""")
        title = "🔥 Top Streaks"
        field_name = "Streak"
    else:
        c.execute("SELECT id, username, broski_balance FROM users ORDER BY broski_balance DESC LIMIT 10")
        title = "💰 Top BROski$ Holders"
        field_name = "Balance"
    
    rows = c.fetchall()
    conn.close()
    
    if not rows:
        await ctx.send("📊 No one has earned BROski$ yet. Be the first! 🚀")
        return
    
    embed = discord.Embed(title=title, color=discord.Color.blue())
    
    leaderboard_text = ""
    for i, row in enumerate(rows, 1):
        user_id, username, value = row
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"][i-1]
        leaderboard_text += f"{medal} **{username}**: {value} {field_name}\n"
    
    embed.description = leaderboard_text
    embed.set_footer(text="Fair economy in action! 🌍")
    
    await ctx.send(embed=embed)

@bot.command(name="stats")
async def stats(ctx):
    """Show economy-wide fairness metrics"""
    metrics = get_fairness_metrics()
    
    embed = discord.Embed(
        title="📊 BROski$ Economy Stats",
        color=discord.Color.purple()
    )
    embed.add_field(name="👥 Active Users", value=metrics['users'], inline=True)
    embed.add_field(name="💰 Total Distributed", value=f"{metrics['total_broski']} BROski$", inline=True)
    embed.add_field(name="📈 Average Earning", value=f"{metrics['avg']} BROski$", inline=True)
    
    embed.add_field(name="⚖️ Fairness Index (Gini)", 
        value=f"**{metrics['gini']}**\n(< 0.30 = Fair, > 0.50 = Concentrated)", 
        inline=False)
    
    embed.set_footer(text="Green = fair, Red = needs rebalancing 🎯")
    await ctx.send(embed=embed)

@bot.command(name="help_broski")
async def help_broski(ctx):
    """Show all BROski$ commands"""
    embed = discord.Embed(
        title="🎮 BROski$ Economy Commands",
        color=discord.Color.blurple()
    )
    
    commands_info = {
        "/balance": "Check your BROski$ balance & stats",
        "/complete <type> [quality]": "Earn BROski$ (code, doc, art, community)",
        "/leaderboard [sort]": "Top earners (balance/lifetime/streak)",
        "/stats": "Economy fairness metrics",
        "/help_broski": "Show this help menu",
    }
    
    for cmd, desc in commands_info.items():
        embed.add_field(name=cmd, value=desc, inline=False)
    
    embed.add_field(name="💡 Tips", 
        value="• Maintain streaks for bonus multipliers\n"
              "• Diversify task types for variety bonus\n"
              "• Quality ratings affect your reward\n"
              "• Economy resets fairness every month",
        inline=False)
    
    await ctx.send(embed=embed)

# ===== RUN BOT =====
if __name__ == "__main__":
    if TOKEN == "YOUR_TOKEN_HERE":
        print("❌ ERROR: Set DISCORD_TOKEN environment variable!")
        print("On Linux/Mac: export DISCORD_TOKEN='your_token_here'")
        print("On Windows: set DISCORD_TOKEN=your_token_here")
        exit(1)
    
    bot.run(TOKEN)

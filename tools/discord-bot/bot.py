import discord
from discord import app_commands
from discord.ext import commands
import os
import subprocess
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 HyperCode Bot is online as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

@bot.tree.command(name="validate", description="Validate HyperCode syntax (paste code or attach .hc file)")
@app_commands.describe(code="Paste your HyperCode snippet here")
async def validate(interaction: discord.Interaction, code: str = None):
    await interaction.response.defer()
    
    source_code = ""
    
    # Handle File Attachment
    if not code and interaction.namespace.file:
        # Note: app_commands doesn't support file upload directly in arguments easily in all versions, 
        # checking message attachments is safer if command was triggered via message, 
        # but slash commands send attachments differently.
        # For MVP, let's rely on the 'code' argument string.
        pass
        
    if code:
        source_code = code
    else:
        await interaction.followup.send("❌ Please provide code to validate!")
        return

    # Create temp file
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.hc', delete=False, encoding='utf-8') as temp:
        temp.write("#:domain classical\n") # Auto-add domain if missing for snippet validity, or let validator catch it
        if "#:domain" in source_code:
             # Overwrite if user provided it
             temp.seek(0)
             temp.truncate()
             temp.write(source_code)
        else:
             temp.write(source_code)
        temp_path = temp.name

    # Run Validator
    try:
        # Pointing to the tools directory relative to where bot runs
        # Assuming bot runs from project root
        validator_path = os.path.join("tools", "code", "syntax_validator.py")
        
        result = subprocess.run(
            ["python", validator_path, temp_path],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        output = result.stdout
        # Clean up ANSI codes for Discord
        clean_output = output.replace('\033[95m', '').replace('\033[94m', '').replace('\033[96m', '')\
                             .replace('\033[92m', '').replace('\033[93m', '').replace('\033[91m', '')\
                             .replace('\033[0m', '').replace('\033[1m', '').replace('\033[4m', '')
        
        emoji = "✅" if result.returncode == 0 else "❌"
        
        response = f"### {emoji} Syntax Validation Result\n```yaml\n{clean_output}\n```"
        await interaction.followup.send(response)
        
    except Exception as e:
        await interaction.followup.send(f"❌ Error running validator: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@bot.tree.command(name="tutorial", description="Get a HyperCode tutorial")
@app_commands.describe(name="Name of the tutorial (e.g., 01_quantum_hello)")
async def tutorial(interaction: discord.Interaction, name: str = "01_quantum_hello"):
    tutorial_path = os.path.join("tutorials", f"{name}.hc")
    
    if not os.path.exists(tutorial_path):
        await interaction.response.send_message(f"❌ Tutorial `{name}` not found. Try `01_quantum_hello`.", ephemeral=True)
        return

    with open(tutorial_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split content to avoid max length
    if len(content) > 1900:
        content = content[:1900] + "\n... (truncated)"

    await interaction.response.send_message(f"### 📚 Tutorial: {name}\n```python\n{content}\n```")

@bot.tree.command(name="docs", description="Fetch latest API documentation")
async def docs(interaction: discord.Interaction):
    await interaction.response.defer()
    
    # Run doc gen
    doc_gen_path = os.path.join("tools", "research", "doc_gen.py")
    output_path = os.path.join("docs", "TEMP_DISCORD_API.md")
    
    subprocess.run(["python", doc_gen_path, "examples/", output_path])
    
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Just send a summary or link
        summary = "### 📚 HyperCode API Reference\n"
        summary += "Full docs available at: https://welshDog.github.io/THE-HYPERCODE/\n\n"
        summary += "**Recent Circuits:**\n"
        if "bell_pair" in content: summary += "- `bell_pair`\n"
        if "grover" in content: summary += "- `grover`\n"
        
        await interaction.followup.send(summary)
    else:
        await interaction.followup.send("❌ Failed to generate docs.")

@bot.tree.command(name="help", description="Show HyperCode Bot commands")
async def help(interaction: discord.Interaction):
    msg = """
### 🤖 HyperCode Bot Commands
- `/validate <code>`: Check your HyperCode syntax.
- `/tutorial [name]`: Get tutorial code (try `01_quantum_hello`).
- `/docs`: Get link to API docs.
    """
    await interaction.response.send_message(msg)

if __name__ == "__main__":
    if not TOKEN or TOKEN == "your_token_here":
        print("❌ Error: DISCORD_TOKEN not set in .env")
    else:
        bot.run(TOKEN)

require('dotenv').config();
const { Client, GatewayIntentBits, Collection, REST, Routes } = require('discord.js');
const mongoose = require('mongoose');
const fs = require('fs');
const path = require('path');
const express = require('express');
const cors = require('cors');
const axios = require('axios'); // For OAuth
const { URLSearchParams } = require('url');

const User = require('./models/User'); // Import User model for API
const Streak = require('./models/Streak'); // Import Streak model for API
const Session = require('./models/Session'); // Import Session model for API

// Initialize Client
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.GuildVoiceStates
  ]
});

// Initialize Express API
const app = express();
const PORT = process.env.PORT || process.env.API_PORT || 3000;

app.use(cors({
  origin: process.env.FRONTEND_URL ? [process.env.FRONTEND_URL, 'http://localhost:5173'] : '*',
  methods: ['GET', 'POST']
}));
app.use(express.json());

// 🏥 HEALTH CHECK ENDPOINT (Combined Bot & DB Status)
app.get('/health', (req, res) => {
  const healthcheck = {
    status: 'ok',
    uptime: process.uptime(),
    timestamp: Date.now(),
    services: {
      database: mongoose.connection.readyState === 1 ? 'connected' : 'disconnected',
      discord: client.ws.status === 0 ? 'connected' : 'disconnected',
      discord_ping: `${client.ws.ping}ms`
    }
  };

  // If critical services are down, return 503
  if (healthcheck.services.database === 'disconnected' && healthcheck.services.discord === 'disconnected') {
    healthcheck.status = 'critical_failure';
    return res.status(503).json(healthcheck);
  }

  res.status(200).json(healthcheck);
});

const aiCoach = require('./utils/aiCoach');

// ... (Existing Imports)

// 🧠 NEW: AI Coach Advice Endpoint
app.get('/api/coach/advice/:userId', async (req, res) => {
  try {
    const { userId } = req.params;

    // Fetch context (Reuse logic from coach command roughly)
    const user = await User.findOne({ discordId: userId }) || { currentStreak: 0, totalFocusTime: 0 };

    // Check active session
    const activeSession = await Session.findOne({ userId, status: 'active' });

    const context = {
      userId,
      username: user.username || 'Warrior',
      currentStreak: user.currentStreak,
      totalFocusTime: user.totalFocusTime,
      isSessionActive: !!activeSession,
    };

    if (activeSession) {
      const durationMs = Date.now() - activeSession.startTime;
      context.sessionDuration = durationMs / 60000;
    }

    const advice = await aiCoach.getAdvice(context);
    res.json({ advice });

  } catch (error) {
    console.error('API Advice Error:', error);
    res.status(500).json({ error: 'Failed to get advice' });
  }
});

// API Endpoints
app.get('/api/stats/:userId', async (req, res) => {
  try {
    let user;
    if (mongoose.connection.readyState === 1) {
      user = await User.findOne({ discordId: req.params.userId });
    } else {
      console.log('⚠️ MongoDB not connected. Serving Mock Data.');
      user = {
        broskiBalance: 150,
        currentStreak: 5,
        totalEarned: 1500,
        discordId: req.params.userId
      };
    }

    if (!user && mongoose.connection.readyState === 1) return res.status(404).json({ error: 'User not found' });
    if (!user) user = { broskiBalance: 0, currentStreak: 0, totalEarned: 0 }; // Default for mock

    // Calculate global rank
    let rank = 1;
    let streakHistory = [];
    if (mongoose.connection.readyState === 1) {
      const allUsers = await User.find().sort({ broskiBalance: -1 });
      rank = allUsers.findIndex(u => u.discordId === req.params.userId) + 1;

      // Fetch Streak History (Last 30 days)
      const thirtyDaysAgo = new Date();
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
      streakHistory = await Streak.find({
        userId: req.params.userId,
        date: { $gte: thirtyDaysAgo }
      }).select('date activityCount -_id');
    }

    res.json({
      balance: user.broskiBalance,
      streak: user.currentStreak,
      rank: rank,
      totalEarned: user.totalEarned,
      history: streakHistory
    });
  } catch (err) {
    console.error("API Error:", err);
    // Fallback to mock data on error
    res.json({
      balance: 100,
      streak: 3,
      rank: 99,
      totalEarned: 300,
      note: "Fallback Data (DB Error)"
    });
  }
});

// Leaderboard Endpoint
app.get('/api/leaderboard', async (req, res) => {
  try {
    const topUsers = await User.find().sort({ broskiBalance: -1 }).limit(10);
    res.json(topUsers.map(u => ({
      discordId: u.discordId,
      username: u.username || 'Unknown', // Make sure to save username in DB or fetch from Discord
      balance: u.broskiBalance,
      streak: u.currentStreak
    })));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Start Express Server IMMEDIATELY (Don't wait for Mongo)
const server = app.listen(PORT, '0.0.0.0', () => {
  console.log(`🌍 BROski API running on http://localhost:${PORT}`);
});

// Database Connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/broski-bot', {
  serverSelectionTimeoutMS: 5000, // Fail after 5 seconds if no server found
  socketTimeoutMS: 45000, // Close sockets after 45 seconds of inactivity
})
  .then(() => console.log('✅ Connected to MongoDB'))
  .catch(err => console.warn('❌ MongoDB Connection Error (Running in Mock Mode):', err.message));

// ==========================================
// 🔐 OAUTH ENDPOINTS
// ==========================================

// 1. Redirect to Discord Login
app.get('/api/auth/login', (req, res) => {
  const clientId = process.env.DISCORD_CLIENT_ID || client.user?.id;
  if (!clientId) return res.status(500).json({ error: "Missing DISCORD_CLIENT_ID" });

  const redirectUri = encodeURIComponent(process.env.DISCORD_REDIRECT_URI || 'http://localhost:5173/auth/callback');
  const url = `https://discord.com/api/oauth2/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=code&scope=identify%20guilds`;

  res.json({ url });
});

// 2. Exchange Code for Token
app.post('/api/auth/exchange', async (req, res) => {
  const { code } = req.body;
  if (!code) return res.status(400).json({ error: 'No code provided' });

  // Mock Mode if Secret is missing
  if (!process.env.DISCORD_CLIENT_SECRET) {
    console.log('⚠️ No Client Secret found. Returning MOCK Auth data.');
    return res.json({
      user: {
        id: '418075243404591106', // Mock ID (Lyndz)
        username: 'HyperUser (Mock)',
        avatar: null
      },
      token: 'mock_token_123'
    });
  }

  try {
    const params = new URLSearchParams({
      client_id: process.env.DISCORD_CLIENT_ID,
      client_secret: process.env.DISCORD_CLIENT_SECRET,
      grant_type: 'authorization_code',
      code,
      redirect_uri: process.env.DISCORD_REDIRECT_URI || 'http://localhost:5173/auth/callback'
    });

    const tokenRes = await axios.post('https://discord.com/api/oauth2/token', params.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });

    const { access_token } = tokenRes.data;

    // Get User Info
    const userRes = await axios.get('https://discord.com/api/users/@me', {
      headers: { Authorization: `Bearer ${access_token}` }
    });

    res.json({
      user: userRes.data,
      token: access_token
    });

  } catch (err) {
    console.error('OAuth Error:', err.response?.data || err.message);
    res.status(500).json({ error: 'Authentication failed' });
  }
});

client.commands = new Collection();

// Load Commands
const commandsPath = path.join(__dirname, 'commands');
const commandFiles = fs.readdirSync(commandsPath).filter(file => file.endsWith('.js'));

const commands = [];

for (const file of commandFiles) {
  const filePath = path.join(commandsPath, file);
  const command = require(filePath);
  if ('data' in command && 'execute' in command) {
    client.commands.set(command.data.name, command);
    commands.push(command.data.toJSON());
  } else {
    console.log(`[WARNING] The command at ${filePath} is missing a required "data" or "execute" property.`);
  }
}

// Event Handling
client.once('ready', async () => {
  console.log(`🤖 BROski Bot Online! Logged in as ${client.user.tag}`);

  // Register Slash Commands
  const rest = new REST({ version: '10' }).setToken(process.env.DISCORD_TOKEN);
  const clientId = client.user.id;

  try {
    console.log('🔄 Refreshing application (/) commands...');

    // Strategy: If GUILD_ID is present, register there.
    // If NOT present, register in ALL guilds the bot is currently in (Best for testing)
    const guildId = process.env.GUILD_ID;

    if (guildId) {
      console.log(`🎯 Registering commands for Guild: ${guildId}`);
      await rest.put(
        Routes.applicationGuildCommands(clientId, guildId),
        { body: commands },
      );
    } else {
      console.log('🌐 No GUILD_ID in .env. Registering commands for ALL joined guilds (Dev Mode)...');
      const guilds = client.guilds.cache.map(g => g.id);
      if (guilds.length === 0) {
        console.log('⚠️ Bot is not in any guilds yet. Invite it using the URL generated in Developer Portal!');
      }
      for (const gId of guilds) {
        console.log(`   - Registering for guild: ${gId}`);
        await rest.put(
          Routes.applicationGuildCommands(clientId, gId),
          { body: commands },
        );
      }
    }
    console.log('✅ Successfully reloaded application (/) commands.');
  } catch (error) {
    console.error('❌ Command Registration Failed:', error);
  }
});

client.on('interactionCreate', async interaction => {
  const command = client.commands.get(interaction.commandName);
  if (!command) return;

  // Handle Autocomplete
  if (interaction.isAutocomplete()) {
    try {
      await command.autocomplete(interaction);
    } catch (error) {
      console.error('Autocomplete Error:', error);
    }
    return;
  }

  if (!interaction.isChatInputCommand()) return;

  try {
    await command.execute(interaction);
  } catch (error) {
    console.error(error);
    if (interaction.replied || interaction.deferred) {
      await interaction.followUp({ content: 'There was an error while executing this command!', ephemeral: true }).catch(e => console.error("Failed to follow up error:", e.message));
    } else {
      await interaction.reply({ content: 'There was an error while executing this command!', ephemeral: true }).catch(e => console.error("Failed to reply error:", e.message));
    }
  }
});

// Prevent crash on unhandled rejections
process.on('unhandledRejection', error => {
  console.error('Unhandled promise rejection:', error);
});

// Login
if (process.env.DISCORD_TOKEN) {
  client.login(process.env.DISCORD_TOKEN);
} else {
  console.log("⚠️ DISCORD_TOKEN not set. Bot will not login.");
}

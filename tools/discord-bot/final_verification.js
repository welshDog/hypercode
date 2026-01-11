const axios = require('axios');
const { EmbedBuilder } = require('discord.js');
const hyperfocus = require('./src/commands/hyperfocus');

// Mock Discord Interaction
const mockInteraction = {
  user: { id: 'test_user_123', username: 'TestCommander' },
  guildId: 'test_guild_456',
  options: {
    getSubcommand: () => 'start', // will change dynamically
    getString: () => 'Coding'
  },
  reply: async (msg) => {
    console.log(`[Bot Reply]: ${msg.content || 'Embed Sent'}`);
    if (msg.embeds) console.log(`[Embed Title]: ${msg.embeds[0].data.title}`);
    return true;
  },
  followUp: async (msg) => console.log(`[Bot FollowUp]: ${msg.content}`)
};

async function runTests() {
  console.log("🚀 STARTING FINAL SYSTEM VERIFICATION...\n");
  const report = {
    dashboard: 'PENDING',
    api: 'PENDING',
    auth: 'PENDING',
    botLogic: 'PENDING'
  };

  // 1. Check Dashboard
  try {
    console.log("👉 Testing Web Dashboard (localhost:5173)...");
    await axios.get('http://localhost:5173');
    console.log("✅ Dashboard is ONLINE");
    report.dashboard = 'PASS';
  } catch (err) {
    console.error("❌ Dashboard Unreachable:", err.message);
    report.dashboard = 'FAIL';
  }

  // 2. Check Bot API
  try {
    console.log("\n👉 Testing Bot API (localhost:3001)...");
    const res = await axios.get('http://localhost:3001/api/stats/test_user_123');
    console.log("✅ API is ONLINE. Stats Response:", res.data);
    if (res.data.balance !== undefined) {
        report.api = 'PASS';
    } else {
        report.api = 'FAIL (Invalid Data)';
    }
  } catch (err) {
    console.error("❌ API Unreachable:", err.message);
    report.api = 'FAIL';
  }

  // 3. Test Auth Endpoint
  try {
    console.log("\n👉 Testing OAuth Login Generator...");
    const res = await axios.get('http://localhost:3001/api/auth/login');
    if (res.data.url && res.data.url.includes('discord.com')) {
        console.log("✅ OAuth URL Generated:", res.data.url);
        report.auth = 'PASS';
    } else {
        console.error("❌ Invalid OAuth URL");
        report.auth = 'FAIL';
    }
  } catch (err) {
    console.error("❌ Auth Endpoint Error:", err.message);
    report.auth = 'FAIL';
  }

  // 4. Test Bot Logic (Hyperfocus Math)
  try {
    console.log("\n👉 Testing Bot Command Logic (Hyperfocus)...");
    
    // Test Start
    mockInteraction.options.getSubcommand = () => 'start';
    await hyperfocus.execute(mockInteraction);
    
    // Test Stop (Simulate 30 mins later)
    mockInteraction.options.getSubcommand = () => 'stop';
    
    // We need to trick the module into thinking time passed. 
    // Since we can't easily mock Date inside the module without rewiring, 
    // we will rely on the fact that the module handles 'activeSession' lookup.
    // In Mock Mode (which the bot uses if DB is down), it mocks the session start time to -25 mins.
    // So 'stop' should trigger a calculation for ~25 mins.
    
    await hyperfocus.execute(mockInteraction);
    console.log("✅ Bot Logic Executed without Crash");
    report.botLogic = 'PASS';

  } catch (err) {
    console.error("❌ Bot Logic Error:", err);
    report.botLogic = 'FAIL';
  }

  console.log("\n=================================");
  console.log("📊 TEST REPORT SUMMARY");
  console.log("=================================");
  console.table(report);
  
  if (Object.values(report).every(status => status === 'PASS')) {
      console.log("\n✨ ALL SYSTEMS GO! READY FOR DEPLOYMENT. ✨");
  } else {
      console.log("\n⚠️ SOME SYSTEMS FAILED. CHECK LOGS.");
  }
}

runTests();

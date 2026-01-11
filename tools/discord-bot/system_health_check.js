const mongoose = require('mongoose');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '.env') });

// Colors for console
const colors = {
  reset: "\x1b[0m",
  green: "\x1b[32m",
  red: "\x1b[31m",
  yellow: "\x1b[33m",
  cyan: "\x1b[36m",
  bold: "\x1b[1m"
};

const log = (msg, color = colors.reset) => console.log(`${color}${msg}${colors.reset}`);

async function runSystemCheck() {
  log(`\n🚀 HYPERCODE SYSTEM DIAGNOSTIC - ${new Date().toISOString()}`, colors.bold + colors.cyan);
  log("==================================================\n");

  const report = {
    database: { status: 'PENDING', latency: 'N/A' },
    api: { status: 'PENDING', endpoints: {} },
    bot: { status: 'PENDING', logic: 'PENDING' },
    frontend: { status: 'PENDING' }
  };

  // 1. DATABASE CHECK
  log("1️⃣  Testing Database Connection...", colors.yellow);
  const startDb = Date.now();
  try {
    if (!process.env.MONGODB_URI) throw new Error("MONGODB_URI missing in .env");
    await mongoose.connect(process.env.MONGODB_URI, { serverSelectionTimeoutMS: 5000 });
    const latency = Date.now() - startDb;
    log(`   ✅ Connected to MongoDB Atlas (${latency}ms)`, colors.green);
    report.database.status = 'PASS';
    report.database.latency = `${latency}ms`;

    // Verify Models
    const collections = Object.keys(mongoose.connection.collections);
    log(`   📂 Collections Found: ${collections.join(', ')}`, colors.cyan);

  } catch (err) {
    log(`   ❌ Database Error: ${err.message}`, colors.red);
    report.database.status = 'FAIL';
  }

  // 2. API ENDPOINT CHECK
  log("\n2️⃣  Testing Local API Endpoints...", colors.yellow);
  const endpoints = [
    { name: 'Stats (Mock User)', url: 'http://localhost:3001/api/stats/system_check_user' },
    { name: 'Auth Login', url: 'http://localhost:3001/api/auth/login' },
    { name: 'Leaderboard', url: 'http://localhost:3001/api/leaderboard' }
  ];

  for (const ep of endpoints) {
    try {
      const startApi = Date.now();
      const res = await axios.get(ep.url);
      const latency = Date.now() - startApi;
      log(`   ✅ ${ep.name}: 200 OK (${latency}ms)`, colors.green);
      report.api.endpoints[ep.name] = 'PASS';
    } catch (err) {
      log(`   ❌ ${ep.name}: ${err.message}`, colors.red);
      report.api.endpoints[ep.name] = 'FAIL';
    }
  }

  // 3. BOT LOGIC SIMULATION
  log("\n3️⃣  Verifying Bot Logic Modules...", colors.yellow);
  try {
    const hyperfocus = require('./src/commands/hyperfocus');
    if (hyperfocus.data.name === 'hyperfocus') {
      log("   ✅ Command Module 'hyperfocus' loaded", colors.green);
    } else {
      throw new Error("Hyperfocus command name mismatch");
    }

    const coach = require('./src/commands/coach');
    if (coach.data.name === 'coach') {
      log("   ✅ Command Module 'coach' loaded", colors.green);
    }

    // TYCOON CHECK
    const shop = require('./src/commands/shop');
    if (shop.data.name === 'shop') {
      log("   ✅ Command Module 'shop' loaded", colors.green);
    }

    // Check if Shop is seeded
    if (report.database.status === 'PASS') {
      const ShopItem = require('./src/models/ShopItem');
      const itemCount = await ShopItem.countDocuments();
      if (itemCount > 0) {
        log(`   ✅ Shop Inventory: ${itemCount} items found`, colors.green);
      } else {
        log(`   ⚠️ Shop is empty! Run 'npm run seed'`, colors.yellow);
      }
    }

    report.bot.status = 'PASS';
  } catch (err) {
    log(`   ❌ Bot Module Error: ${err.message}`, colors.red);
    report.bot.status = 'FAIL';
  }

  // 4. FRONTEND BUILD CHECK
  log("\n4️⃣  Checking Dashboard Integrity...", colors.yellow);
  const dashboardPath = path.resolve(__dirname, '../../web/dashboard');
  if (fs.existsSync(path.join(dashboardPath, 'package.json'))) {
    log("   ✅ Dashboard Project Found", colors.green);
    if (fs.existsSync(path.join(dashboardPath, 'src/components/StreakCalendar.jsx'))) {
      log("   ✅ StreakCalendar Component Verified", colors.green);
      report.frontend.status = 'PASS';
    } else {
      log("   ⚠️ StreakCalendar Missing", colors.red);
      report.frontend.status = 'PARTIAL';
    }
  } else {
    log("   ❌ Dashboard Directory Missing", colors.red);
    report.frontend.status = 'FAIL';
  }

  // SUMMARY
  log("\n==================================================", colors.cyan);
  log("📊 DIAGNOSTIC SUMMARY", colors.bold);
  console.table(report);

  // Cleanup
  await mongoose.disconnect();
  log("\n✅ Check Complete. Exiting.", colors.cyan);
}

runSystemCheck();

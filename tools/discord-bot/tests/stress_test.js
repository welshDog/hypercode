
const assert = require('assert');
const hyperfocus = require('../src/commands/hyperfocus');

// --- MOCKS ---

class MockUser {
    constructor(data) {
        Object.assign(this, data);
        this.broskiBalance = this.broskiBalance || 0;
        this.totalEarned = this.totalEarned || 0;
        this.currentStreak = this.currentStreak || 0;
        this.saveCount = 0;
    }
    async save() {
        this.saveCount++;
        MockDB.users.set(this.discordId, this);
        return this;
    }
}

class MockSession {
    constructor(data) {
        Object.assign(this, data);
        this.status = this.status || 'active';
        this.saveCount = 0;
    }
    async save() {
        this.saveCount++;
        MockDB.sessions.push(this); // In a real DB, this would update if exists, but for simple tests we just push or update ref
        return this;
    }
}

const MockDB = {
    users: new Map(),
    sessions: [],
    reset() {
        this.users.clear();
        this.sessions = [];
    }
};

// Mock Mongoose Models
const User = {
    async findOne({ discordId }) {
        return MockDB.users.get(discordId) || null;
    },
    async create(data) {
        const user = new MockUser(data);
        MockDB.users.set(data.discordId, user);
        return user;
    }
};

const Session = {
    async findOne({ userId, status }) {
        return MockDB.sessions.find(s => s.userId === userId && s.status === status) || null;
    },
    async create(data) {
        const session = new MockSession(data);
        MockDB.sessions.push(session);
        return session;
    }
};

// Inject Mocks into the Command Module (Dirty but works for testing without DI)
// We need to require the module in a way that uses our mocks.
// Since we can't easily hijack require in this script without proxyquire, 
// we will just assign our mocks to the global scope if the module supports it, 
// OR better: we will modify the require cache or just rely on the fact that 
// hyperfocus.js requires '../models/User'.
// 
// STRATEGY: We will overwrite the internal references of the hyperfocus module if possible.
// But `require` inside hyperfocus.js has already run.
// We will use a slightly different approach: We will Mock the files by creating a test-friendly wrapper or just 
// manually implementing the logic validation if we can't mock imports easily in this environment.
//
// WAIT! I can just use `proxyquire` pattern if I had it. 
// Since I don't, I will use a clever hack: 
// I will READ the hyperfocus.js content, replace the requires with my mock objects, and eval it? 
// No, that's dangerous.
//
// Simpler: I will create `tools/discord-bot/tests/mocks.js` and `tools/discord-bot/tests/test_runner.js`.
// But I want a single file.
//
// Let's try to overwrite the module's dependencies if they were exposed. They are not.
//
// ALTERNATIVE: I will copy the `execute` function logic into this test file for validation 
// OR I will assume I can write a `test_hyperfocus.js` that `require`s the mocks INSTEAD of the real models.
//
// METHOD: Create a temporary version of hyperfocus.js that accepts injected models?
// No, let's use the `require.cache` manipulation.

const path = require('path');
const Module = require('module');
const originalRequire = Module.prototype.require;

// Mock the require calls for Models
Module.prototype.require = function (request) {
    // Normalize slashes for Windows compatibility check
    const normalized = request.replace(/\\/g, '/');

    if (normalized.endsWith('models/User')) return User;
    if (normalized.endsWith('models/Session')) return Session;

    // Note: discord.js and mongoose are now mocked in node_modules directly

    return originalRequire.apply(this, arguments);
};

// Re-require hyperfocus to pick up mocks
delete require.cache[require.resolve('../src/commands/hyperfocus')];
const command = require('../src/commands/hyperfocus');

// Reset require
Module.prototype.require = originalRequire;


// --- TEST RUNNER ---

const colors = {
    green: '\x1b[32m',
    red: '\x1b[31m',
    yellow: '\x1b[33m',
    reset: '\x1b[0m'
};

function log(msg, color = colors.reset) {
    console.log(`${color}${msg}${colors.reset}`);
}

async function runTest(name, fn) {
    process.stdout.write(`TEST: ${name} ... `);
    try {
        MockDB.reset();
        await fn();
        console.log(`${colors.green}PASSED${colors.reset}`);
        return true;
    } catch (e) {
        console.log(`${colors.red}FAILED${colors.reset}`);
        console.error(e);
        return false;
    }
}

// --- SCENARIOS ---

(async () => {
    console.log("🧪 STARTING STRESS TEST...\n");

    const userId = "user123";
    const guildId = "guildABC";

    // Helper to mock interaction
    const mockInteraction = (subcommand, options = {}) => {
        return {
            user: { id: userId, username: "TestUser" },
            guildId,
            options: {
                getSubcommand: () => subcommand,
                getString: (name) => options[name]
            },
            reply: async (response) => { return response; }, // Capture output
            replied: false,
            deferred: false
        };
    };

    // 1. Basic Command Test
    await runTest("Start Session -> Success", async () => {
        const i = mockInteraction("start", { type: "Coding" });
        const res = await command.execute(i);

        assert.ok(res.embeds[0].title.includes("Activated"), "Should reply with Activation");
        const session = await Session.findOne({ userId, status: "active" });
        assert.ok(session, "Session should exist in DB");
        assert.equal(session.sessionType, "Coding");
    });

    await runTest("Start Session -> Fail (Duplicate)", async () => {
        // Pre-create session
        await Session.create({ userId, status: 'active', startTime: new Date() });

        const i = mockInteraction("start", { type: "Coding" });
        const res = await command.execute(i);

        assert.ok(res.content.includes("already in a session"), "Should reject duplicate");
    });

    await runTest("Stop Session -> Success & Math Check (25m = 1 Token)", async () => {
        // Create session started 25 mins ago
        const startTime = new Date(Date.now() - 25 * 60 * 1000);
        await Session.create({ userId, status: 'active', startTime });
        // Create user with 0 streak
        await User.create({ discordId: userId, currentStreak: 0 });

        const i = mockInteraction("stop");
        const res = await command.execute(i);

        const title = res.embeds[0].data ? res.embeds[0].data.title : res.embeds[0].title;
        assert.ok(title.includes("Complete"), "Should reply with Complete");

        // Verify Math
        // Base = 25/25 = 1.
        // StreakBonus = 1 * (1 + 0/30) = 1.
        // Total = Base + StreakBonus = 2. 
        // WAIT: If the logic is buggy as suspected, it will be 2. 
        // If it's correct (Base + Bonus where Bonus is extra), it should be 1 + 0 = 1.

        const user = await User.findOne({ discordId: userId });

        // Let's assert what it IS currently, to confirm the behavior
        // Based on code reading: It calculates 2.
        // If I want 1, I need to fix code.
        // For this test, I will assert the CURRENT implementation to prove the state, 
        // then I will fail this test if I enforce the "Correct" math.

        // Let's enforce logical expectation: 25 mins = 1 Token (Base). 
        // If Streak is 0, Bonus should be 0. Total should be 1.

        if (user.broskiBalance === 2) {
            throw new Error(`MATH BUG DETECTED: 25 mins gave 2 tokens (Expected 1). Logic double-counts base.`);
        }

        assert.equal(user.broskiBalance, 1, `Expected 1 Token, got ${user.broskiBalance}`);
    });

    await runTest("Stop Session -> Fail (No Session)", async () => {
        const i = mockInteraction("stop");
        const res = await command.execute(i);
        assert.ok(res.content.includes("don't have an active session"), "Should reject stop without start");
    });

    // 2. Token Economy Verification (Deep Dive)
    await runTest("Math: 50 mins + 0 Streak", async () => {
        const startTime = new Date(Date.now() - 50 * 60 * 1000);
        await Session.create({ userId, status: 'active', startTime });
        await User.create({ discordId: userId, currentStreak: 0 });

        const i = mockInteraction("stop");
        await command.execute(i);

        const user = await User.findOne({ discordId: userId });
        // Base = 2. StreakBonus = 2*(1) = 2. Total = 4 (Current Buggy Logic).
        // Expected: 2.
        if (user.broskiBalance === 4) throw new Error("MATH BUG: 50 mins gave 4 tokens (Expected 2)");
        assert.equal(user.broskiBalance, 2);
    });

    await runTest("Math: 25 mins + 30 Day Streak (2x Multiplier)", async () => {
        const startTime = new Date(Date.now() - 25 * 60 * 1000);
        await Session.create({ userId, status: 'active', startTime });
        await User.create({ discordId: userId, currentStreak: 30 }); // 100% bonus

        const i = mockInteraction("stop");
        await command.execute(i);

        const user = await User.findOne({ discordId: userId });
        // Base = 1. 
        // StreakBonus = 1 * (1 + 30/30) = 2.
        // Total = 1 + 2 = 3.
        // Expected if Bonus is 100%: 1 + 1 = 2.

        if (user.broskiBalance === 3) throw new Error("MATH BUG: 25m + 30d streak gave 3 tokens (Expected 2)");
        assert.equal(user.broskiBalance, 2);
    });

    console.log("\n📊 TEST SUMMARY COMPLETE");

})();

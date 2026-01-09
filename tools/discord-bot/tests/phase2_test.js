
const assert = require('assert');
// NOTE: We delay require() of our source files until AFTER we mock the dependencies
// because they import discord.js and openai at the top level.

// --- MOCKS ---
const MockDB = {
    users: [],
    sessions: [],
    reset() {
        this.users = [];
        this.sessions = [];
    }
};

const User = {
    async findOne({ discordId }) {
        return MockDB.users.find(u => u.discordId === discordId) || null;
    },
    find() {
        return {
            sort: (criteria) => {
                // Simple in-memory sort
                const key = Object.keys(criteria)[0];
                const dir = criteria[key];
                const sorted = [...MockDB.users].sort((a, b) => {
                    return dir === -1 ? b[key] - a[key] : a[key] - b[key];
                });
                return {
                    limit: (n) => {
                        const limited = sorted.slice(0, n);
                        return {
                            select: () => limited // mock select just returns objects
                        }
                    }
                }
            }
        }
    }
};

const Session = {
    async findOne({ userId, status }) {
        return MockDB.sessions.find(s => s.userId === userId && s.status === status) || null;
    }
};

// Mock Dependencies
const Module = require('module');
const originalRequire = Module.prototype.require;

const MockDiscord = {
    SlashCommandBuilder: class {
        setName() { return this; }
        setDescription() { return this; }
        addSubcommand(fn) {
            const sc = new MockDiscord.SlashCommandBuilder();
            fn(sc);
            return this;
        }
        addStringOption() { return this; }
    },
    EmbedBuilder: class {
        constructor() { this.data = {}; }
        setColor(c) { this.data.color = c; return this; }
        setTitle(t) { this.data.title = t; return this; }
        setDescription(d) { this.data.description = d; return this; }
        addFields(f) { this.data.fields = f; return this; }
        setFooter(f) { this.data.footer = f; return this; }
        // Helper
        get description() { return this.data.description; }
    }
};

const MockOpenAI = class {
    constructor() {
        this.chat = {
            completions: {
                create: async () => ({ choices: [{ message: { content: "AI Advice" } }] })
            }
        };
    }
};

Module.prototype.require = function (request) {
    const normalized = request.replace(/\\/g, '/');
    if (normalized.endsWith('models/User')) return User;
    if (normalized.endsWith('models/Session')) return Session;
    if (request === 'discord.js') return MockDiscord;
    if (request === 'openai') return MockOpenAI;

    return originalRequire.apply(this, arguments);
};

// Re-require modules to pick up mocks
// We need to clear cache for utils/aiCoach because it might have been loaded
delete require.cache[require.resolve('../src/commands/coach')];
delete require.cache[require.resolve('../src/commands/leaderboard')];
try {
    delete require.cache[require.resolve('../src/utils/aiCoach')];
} catch (e) { }

const coach = require('../src/commands/coach');
const leaderboard = require('../src/commands/leaderboard');
const aiCoach = require('../src/utils/aiCoach');


// --- TEST RUNNER ---
const colors = { green: '\x1b[32m', red: '\x1b[31m', reset: '\x1b[0m' };
async function runTest(name, fn) {
    process.stdout.write(`TEST: ${name} ... `);
    try {
        MockDB.reset();
        await fn();
        console.log(`${colors.green}PASSED${colors.reset}`);
    } catch (e) {
        console.log(`${colors.red}FAILED${colors.reset}`);
        console.error(e);
    }
}

(async () => {
    console.log("🧪 PHASE 2 FEATURE TEST...\n");

    const userId = "user123";

    const mockInteraction = (subcommand, options = {}) => {
        return {
            user: { id: userId, username: "TestUser" },
            options: {
                getSubcommand: () => subcommand,
                getString: (name) => options[name]
            },
            deferReply: async () => { },
            editReply: async (res) => res,
            reply: async (res) => res
        };
    };

    // 1. AI Coach Offline Mode
    await runTest("Coach Status (Offline - Short Session)", async () => {
        // Setup: Active session of 12 mins (Target: 25)
        const startTime = new Date(Date.now() - 12 * 60 * 1000);
        MockDB.sessions.push({ userId, status: 'active', startTime, sessionType: 'Coding' });
        MockDB.users.push({ discordId: userId, currentStreak: 5 });

        const i = mockInteraction("status");
        const res = await coach.execute(i);

        // Expectation: "Push 13 more mins"
        const desc = res.embeds[0].data.description;
        assert.ok(desc.includes("13 more mins"), `Expected '13 more mins' in: ${desc}`);
    });

    await runTest("Coach Status (Offline - Streak Hype)", async () => {
        // Setup: No active session, but high streak
        MockDB.users.push({ discordId: userId, currentStreak: 10 });

        const i = mockInteraction("status");
        const res = await coach.execute(i);

        // Expectation: "10-day streak"
        const desc = res.embeds[0].data.description;
        assert.ok(desc.includes("10-day streak"), `Expected '10-day streak' in: ${desc}`);
    });

    // 2. Leaderboard
    await runTest("Leaderboard (Weekly/Streak)", async () => {
        MockDB.users.push(
            { discordId: "u1", username: "Alpha", currentStreak: 5, broskiBalance: 100 },
            { discordId: "u2", username: "Beta", currentStreak: 20, broskiBalance: 50 },
            { discordId: "u3", username: "Gamma", currentStreak: 2, broskiBalance: 200 }
        );

        const i = mockInteraction("weekly");
        const res = await leaderboard.execute(i);

        const desc = res.embeds[0].data.description;
        // Beta (20) should be first
        assert.ok(desc.includes("🥇 Beta"), "Beta should be #1");
        // Alpha (5) second
        assert.ok(desc.includes("🥈 Alpha"), "Alpha should be #2");
    });

    await runTest("Leaderboard (All-Time/Balance)", async () => {
        MockDB.users.push(
            { discordId: "u1", username: "Alpha", currentStreak: 5, broskiBalance: 100 },
            { discordId: "u2", username: "Beta", currentStreak: 20, broskiBalance: 50 },
            { discordId: "u3", username: "Gamma", currentStreak: 2, broskiBalance: 200 }
        );

        const i = mockInteraction("alltime");
        const res = await leaderboard.execute(i);

        const desc = res.embeds[0].data.description;
        // Gamma (200) should be first
        assert.ok(desc.includes("🥇 Gamma"), "Gamma should be #1");
        // Alpha (100) second
        assert.ok(desc.includes("🥈 Alpha"), "Alpha should be #2");
    });

    console.log("\n📊 PHASE 2 TESTS COMPLETE");
})();

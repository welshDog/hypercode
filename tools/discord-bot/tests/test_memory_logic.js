const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });
const mongoose = require('mongoose');
const aiCoach = require('../src/utils/aiCoach');
const AICoachMemory = require('../src/models/AICoachMemory');

async function testMemoryLogic() {
    console.log('🧪 Starting AI Memory Logic Test...');

    // 1. Connect to DB
    if (!process.env.MONGODB_URI) {
        console.error('❌ No MONGODB_URI found in .env');
        process.exit(1);
    }

    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB');

    const testUserId = 'TEST_USER_999';

    // 2. Clear previous test memories
    await AICoachMemory.deleteMany({ userId: testUserId });
    console.log('🧹 Cleared old test memories');

    // 3. Save a "Session Abandoned" memory
    await aiCoach.saveMemory(
        testUserId,
        'SessionSummary',
        'User abandoned session after 5 minutes.'
    );
    console.log('💾 Saved "Abandoned" memory');

    // 4. Verify Memory Fetch
    const memories = await aiCoach.getRecentMemories(testUserId);
    console.log(`🔍 Fetched ${memories.length} memories`);

    if (memories.length > 0 && memories[0].content.includes('abandoned')) {
        console.log('✅ Memory verification passed');
    } else {
        console.error('❌ Memory verification failed');
    }

    // 5. Test Offline Advice Logic
    // Force offline by temporarily unsetting API key (if present)
    const originalKey = process.env.OPENAI_API_KEY;
    delete process.env.OPENAI_API_KEY;
    aiCoach.client = null; // Force null client

    console.log('🤖 Testing Offline Advice Generation...');
    const context = {
        userId: testUserId,
        currentStreak: 5,
        sessionDuration: 0
    };

    const advice = await aiCoach.getAdvice(context);
    console.log(`\n💬 COACH SAYS: "${advice}"\n`);

    if (advice.includes('dropped that last session')) {
        console.log('✅ Context-aware offline advice working!');
    } else {
        console.warn('⚠️ Advice did not match expected context (Random fallback might have triggered if logic is loose)');
    }

    // Cleanup
    process.env.OPENAI_API_KEY = originalKey;
    await mongoose.disconnect();
    console.log('👋 Test Complete');
}

testMemoryLogic();
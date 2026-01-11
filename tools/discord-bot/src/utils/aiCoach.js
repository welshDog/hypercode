const OpenAI = require('openai');
const AICoachMemory = require('../models/AICoachMemory');

class AICoach {
    constructor() {
        this.client = process.env.OPENAI_API_KEY
            ? new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
            : null;

        // Fallback messages for when API is missing or fails
        this.offlineMessages = [
            "🧠 **Coach (Offline Mode):** You're doing great! Keep pushing!",
            "🧠 **Coach (Offline Mode):** Hydrate, bro. It's been a while.",
            "🧠 **Coach (Offline Mode):** Focus is a muscle. You're building it right now.",
            "🧠 **Coach (Offline Mode):** I see that streak! Don't break the chain!"
        ];
    }

    /**
     * Saves a new memory for the AI context
     * @param {string} userId - Discord User ID
     * @param {string} type - 'SessionSummary', 'Goal', 'AdviceGiven'
     * @param {string} content - The text content
     */
    async saveMemory(userId, type, content) {
        try {
            await AICoachMemory.create({
                userId,
                type,
                content,
                createdAt: new Date()
            });
            console.log(`[AI Memory] Saved: ${type} for ${userId}`);
        } catch (error) {
            console.error('[AI Memory] Save Failed:', error.message);
        }
    }

    /**
     * Retrieves recent memories to build context
     * @param {string} userId 
     * @param {number} limit 
     */
    async getRecentMemories(userId, limit = 5) {
        try {
            return await AICoachMemory.find({ userId })
                .sort({ createdAt: -1 })
                .limit(limit);
        } catch (error) {
            console.error('[AI Memory] Fetch Failed:', error.message);
            return [];
        }
    }

    /**
     * Generates a personalized message based on user context
     * @param {Object} context - User stats and session info
     * @returns {Promise<string>}
     */
    async getAdvice(context) {
        // Fetch memories if userId is present
        let memories = [];
        if (context.userId) {
            memories = await this.getRecentMemories(context.userId);
        }

        if (!this.client) {
            return this._getOfflineAdvice(context, memories);
        }

        try {
            const prompt = this._buildPrompt(context, memories);
            const response = await this.client.chat.completions.create({
                model: "gpt-4", // or gpt-3.5-turbo
                messages: [
                    { role: "system", content: "You are 'BROski', a high-energy, supportive, and slightly chaotic ADHD productivity coach. You speak in short, punchy sentences. You use emojis. Your goal is to keep the user in 'Hyperfocus'. If they are close to a milestone, hype them up. If they are struggling, offer a dopamine hack. Use the user's recent history to be specific." },
                    { role: "user", content: prompt }
                ],
                max_tokens: 150,
                temperature: 0.7
            });

            const advice = response.choices[0].message.content;
            
            // Save the advice given to memory
            if (context.userId) {
                await this.saveMemory(context.userId, 'AdviceGiven', advice);
            }

            return advice;
        } catch (error) {
            console.error("OpenAI Error:", error);
            return this._getOfflineAdvice(context, memories);
        }
    }

    _getOfflineAdvice(context, memories) {
        // Simple logic-based responses (No AI)
        const { currentStreak, sessionDuration } = context;

        // 1. Check for recent failures/successes in memory
        if (memories.length > 0) {
            const lastSession = memories.find(m => m.type === 'SessionSummary');
            if (lastSession && lastSession.content.includes('abandoned')) {
                return `🧠 **Coach:** Hey, I saw you dropped that last session. No stress! Let's just do 5 minutes today to get back on track. 🧱`;
            }
        }

        if (sessionDuration && sessionDuration < 25) {
            const needed = 25 - sessionDuration;
            return `🧠 **Coach:** Yo! I see a **${Math.floor(sessionDuration)} min** session. Push **${Math.ceil(needed)} more mins** to hit the multiplier! 🚀`;
        }

        if (currentStreak > 3) {
            return `🧠 **Coach:** You're on a **${currentStreak}-day streak**! You're a machine! Keep it locked! 🔥`;
        }

        return this.offlineMessages[Math.floor(Math.random() * this.offlineMessages.length)];
    }

    _buildPrompt(context, memories) {
        const memoryText = memories.map(m => `[${m.createdAt.toISOString().split('T')[0]}] ${m.type}: ${m.content}`).join('\n');
        
        return JSON.stringify({
            task: "Give advice to this user",
            userStats: context,
            recentHistory: memoryText
        });
    }
}

module.exports = new AICoach();

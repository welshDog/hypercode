const OpenAI = require('openai');

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
     * Generates a personalized message based on user context
     * @param {Object} context - User stats and session info
     * @returns {Promise<string>}
     */
    async getAdvice(context) {
        if (!this.client) {
            return this._getOfflineAdvice(context);
        }

        try {
            const prompt = this._buildPrompt(context);
            const response = await this.client.chat.completions.create({
                model: "gpt-4", // or gpt-3.5-turbo
                messages: [
                    { role: "system", content: "You are 'BROski', a high-energy, supportive, and slightly chaotic ADHD productivity coach. You speak in short, punchy sentences. You use emojis. Your goal is to keep the user in 'Hyperfocus'. If they are close to a milestone, hype them up. If they are struggling, offer a dopamine hack." },
                    { role: "user", content: prompt }
                ],
                max_tokens: 150,
                temperature: 0.7
            });

            return response.choices[0].message.content;
        } catch (error) {
            console.error("OpenAI Error:", error);
            return this._getOfflineAdvice(context);
        }
    }

    _getOfflineAdvice(context) {
        // Simple logic-based responses (No AI)
        const { currentStreak, sessionDuration, sessionType } = context;

        if (sessionDuration && sessionDuration < 25) {
            const needed = 25 - sessionDuration;
            return `🧠 **Coach:** Yo! I see a **${Math.floor(sessionDuration)} min** session. Push **${Math.ceil(needed)} more mins** to hit the multiplier! 🚀`;
        }

        if (currentStreak > 3) {
            return `🧠 **Coach:** You're on a **${currentStreak}-day streak**! You're a machine! Keep it locked! 🔥`;
        }

        return this.offlineMessages[Math.floor(Math.random() * this.offlineMessages.length)];
    }

    _buildPrompt(context) {
        return JSON.stringify({
            task: "Give advice to this user",
            userStats: context
        });
    }
}

module.exports = new AICoach();

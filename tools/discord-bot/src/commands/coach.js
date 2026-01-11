const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const User = require('../models/User');
const Session = require('../models/Session');
const aiCoach = require('../utils/aiCoach');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('coach')
    .setDescription('Get personalized advice from the AI Coach')
    .addSubcommand(subcommand =>
      subcommand
        .setName('status')
        .setDescription('Check your current session and get a hype up')
    )
    .addSubcommand(subcommand =>
      subcommand
        .setName('ask')
        .setDescription('Ask the coach a specific question')
        .addStringOption(option => 
            option.setName('question')
            .setDescription('What do you need help with?')
            .setRequired(true)
        )
    ),

  async execute(interaction) {
    await interaction.deferReply(); // AI might take a second

    const subcommand = interaction.options.getSubcommand();
    const discordId = interaction.user.id;
    
    // Fetch Context
    const user = await User.findOne({ discordId }) || { currentStreak: 0, totalFocusTime: 0 };
    const activeSession = await Session.findOne({ userId: discordId, status: 'active' });

    let context = {
        userId: discordId, // Critical for AI Memory
        username: interaction.user.username,
        currentStreak: user.currentStreak,
        totalFocusTime: user.totalFocusTime,
        isSessionActive: !!activeSession,
    };

    if (activeSession) {
        const durationMs = Date.now() - activeSession.startTime;
        context.sessionDuration = durationMs / 60000; // minutes
        context.sessionType = activeSession.sessionType;
    }

    if (subcommand === 'ask') {
        context.question = interaction.options.getString('question');
    }

    // Get Advice
    const advice = await aiCoach.getAdvice(context);

    // Build Response
    const embed = new EmbedBuilder()
        .setColor('#9b59b6') // Purple for AI
        .setDescription(advice)
        .setFooter({ text: 'Powered by HyperCode AI' });

    if (context.isSessionActive) {
        embed.setTitle('🔥 Hyperfocus Status');
        embed.addFields({ name: 'Current Session', value: `${Math.floor(context.sessionDuration)} mins`, inline: true });
    } else {
        embed.setTitle('🧠 Coach Says...');
    }

    return interaction.editReply({ embeds: [embed] });
  },
};

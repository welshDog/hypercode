const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const User = require('../models/User');
const Session = require('../models/Session');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('hyperfocus')
    .setDescription('Manage your hyperfocus sessions')
    .addSubcommand(subcommand =>
      subcommand
        .setName('start')
        .setDescription('Start a new focus session')
        .addStringOption(option =>
          option.setName('type')
            .setDescription('What are you working on?')
            .setRequired(true)
            .addChoices(
              { name: 'Coding', value: 'Coding' },
              { name: 'Design', value: 'Design' },
              { name: 'Writing', value: 'Writing' },
              { name: 'Learning', value: 'Learning' }
            )
        )
    )
    .addSubcommand(subcommand =>
      subcommand
        .setName('stop')
        .setDescription('End your current focus session')
    ),

  async execute(interaction) {
    const subcommand = interaction.options.getSubcommand();
    const discordId = interaction.user.id;
    const mongoose = require('mongoose');

    // MOCK MODE CHECK
    const isDBConnected = mongoose.connection.readyState === 1;

    // Ensure user exists (Mock or Real)
    let user;
    if (isDBConnected) {
      user = await User.findOne({ discordId });
      if (!user) {
        user = await User.create({
          discordId,
          username: interaction.user.username,
          roles: ['Warrior']
        });
      }
    } else {
      // Mock User
      user = {
        discordId,
        username: interaction.user.username,
        currentStreak: 5, // Mock streak
        broskiBalance: 150
      };
    }

    if (subcommand === 'start') {
      // Check for active session
      let activeSession = null;
      if (isDBConnected) {
        activeSession = await Session.findOne({ userId: discordId, status: 'active' });
      }

      if (activeSession) {
        return interaction.reply({
          content: `⚠️ You're already in a session started at <t:${Math.floor(activeSession.startTime.getTime() / 1000)}:t>! Use \`/hyperfocus stop\` to end it first.`,
          ephemeral: true
        });
      }

      const sessionType = interaction.options.getString('type');

      if (isDBConnected) {
        await Session.create({
          userId: discordId,
          guildId: interaction.guildId,
          startTime: new Date(),
          sessionType,
          status: 'active'
        });
      }

      const embed = new EmbedBuilder()
        .setColor('#00ff00')
        .setTitle('🚀 Hyperfocus Mode Activated')
        .setDescription(`**Focus Target:** ${sessionType}\n\nGood luck, ${interaction.user.username}! I'll track your time and GitHub commits.`)
        .addFields({ name: 'Started At', value: `<t:${Math.floor(Date.now() / 1000)}:t>` })
        .setFooter({ text: isDBConnected ? 'Stay hydrated! 💧' : 'Stay hydrated! 💧 (Offline Mode)' });

      return interaction.reply({ embeds: [embed] });
    }

    if (subcommand === 'stop') {
      let activeSession = null;
      if (isDBConnected) {
        activeSession = await Session.findOne({ userId: discordId, status: 'active' });
      } else {
        // Mock active session for testing
        activeSession = {
          startTime: new Date(Date.now() - 25 * 60000), // Started 25 mins ago
          sessionType: 'Mock Session'
        };
      }

      if (!activeSession) {
        return interaction.reply({
          content: `❌ You don't have an active session! Use \`/hyperfocus start\` to begin one.`,
          ephemeral: true
        });
      }

      const endTime = new Date();
      const durationMs = endTime - activeSession.startTime;
      const durationMinutes = Math.floor(durationMs / 60000);

      // Token Calculation Logic (from Research)
      // Base Tokens = Focus Minutes / 25
      const baseTokens = durationMinutes / 25;

      // Streak Multiplier (1 + Streak/30)
      const streakMultiplier = 1 + (user.currentStreak / 30);

      // Total (rounded to 2 decimals)
      const totalTokens = Math.round((baseTokens * streakMultiplier) * 100) / 100;

      // Update Session
      if (isDBConnected) {
        activeSession.endTime = endTime;
        activeSession.focusMinutes = durationMinutes;
        activeSession.tokensEarned = totalTokens;
        activeSession.status = 'completed';
        await activeSession.save();

        user.broskiBalance += totalTokens;
        user.totalEarned += totalTokens;
        if (user.totalFocusTime) user.totalFocusTime += durationMinutes;
        if (user.sessionCount) user.sessionCount += 1;
        await user.save();
      }

      const embed = new EmbedBuilder()
        .setColor('#ffcc00')
        .setTitle('🏁 Session Complete!')
        .setDescription(`Great work, ${interaction.user.username}!`)
        .addFields(
          { name: '⏱️ Duration', value: `${durationMinutes} minutes`, inline: true },
          { name: '💰 Earned', value: `${totalTokens} BROski$`, inline: true },
          { name: '🔥 Streak', value: `${user.currentStreak} days`, inline: true }
        )
        .setFooter({ text: isDBConnected ? 'Session Saved' : 'Session Completed (Offline Mode - Not Saved)' });

      return interaction.reply({ embeds: [embed] });
    }
  },
};

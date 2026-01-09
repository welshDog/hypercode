const { SlashCommandBuilder, EmbedBuilder } = require('discord.js');
const User = require('../models/User');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('leaderboard')
    .setDescription('See who is dominating the Hyperfocus Zone')
    .addSubcommand(subcommand =>
      subcommand
        .setName('weekly')
        .setDescription('Top users this week')
    )
    .addSubcommand(subcommand =>
      subcommand
        .setName('alltime')
        .setDescription('Legends of the zone')
    ),

  async execute(interaction) {
    const subcommand = interaction.options.getSubcommand();
    
    // Sort criteria
    let sortQuery = { broskiBalance: -1 }; // Default: Richest
    let title = "🏆 All-Time Legends";
    
    // Note: For 'weekly', we'd need to aggregate Session data by date.
    // For this MVP, we will stick to User stats.
    // Ideally, we would have a 'weeklyFocusTime' field on User that resets via cron job,
    // or we run an aggregation on the Session collection.
    
    // Let's do a simple aggregation for Weekly if needed, or just mock it with total for now 
    // to keep it fast, but let's try to be accurate if we can.
    // Actually, simpler MVP: Sort by 'currentStreak' for a "Consistency" board?
    // Let's stick to Balance (All Time) vs Streak (Weekly/Active).
    
    if (subcommand === 'weekly') {
        sortQuery = { currentStreak: -1 };
        title = "🔥 Active Streak Leaders";
    }

    const topUsers = await User.find({})
        .sort(sortQuery)
        .limit(10)
        .select('username broskiBalance currentStreak totalFocusTime');

    if (topUsers.length === 0) {
        return interaction.reply("No data yet! Start focusing to claim #1.");
    }

    // Build the list
    const leaderboardString = topUsers.map((u, index) => {
        const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `#${index + 1}`;
        const score = subcommand === 'weekly' 
            ? `${u.currentStreak} day streak` 
            : `${u.broskiBalance.toFixed(2)} BROski$`;
            
        return `**${medal} ${u.username}** — ${score}`;
    }).join('\n');

    const embed = new EmbedBuilder()
        .setColor('#f1c40f') // Gold
        .setTitle(title)
        .setDescription(leaderboardString)
        .setFooter({ text: 'Grind harder to reach the top!' });

    return interaction.reply({ embeds: [embed] });
  },
};

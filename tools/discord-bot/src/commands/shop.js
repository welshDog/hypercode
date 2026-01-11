const { SlashCommandBuilder, EmbedBuilder, ActionRowBuilder, ButtonBuilder, ButtonStyle } = require('discord.js');
const User = require('../models/User');
const ShopItem = require('../models/ShopItem');
const Transaction = require('../models/Transaction');

module.exports = {
  data: new SlashCommandBuilder()
    .setName('shop')
    .setDescription('Spend your hard-earned BROski$')
    .addSubcommand(subcommand =>
      subcommand
        .setName('browse')
        .setDescription('View available items')
    )
    .addSubcommand(subcommand =>
      subcommand
        .setName('buy')
        .setDescription('Purchase an item')
        .addStringOption(option =>
          option.setName('item')
            .setDescription('Name of the item to buy')
            .setRequired(true)
            .setAutocomplete(true) 
        )
    )
    .addSubcommand(subcommand =>
      subcommand
        .setName('inventory')
        .setDescription('View your owned items')
    ),

  async autocomplete(interaction) {
    const focusedValue = interaction.options.getFocused();
    const items = await ShopItem.find({ isActive: true });
    const filtered = items.filter(choice => choice.name.toLowerCase().includes(focusedValue.toLowerCase()));
    await interaction.respond(
      filtered.map(choice => ({ name: `${choice.name} (${choice.price} $)` , value: choice.name })).slice(0, 25)
    );
  },

  async execute(interaction) {
    const subcommand = interaction.options.getSubcommand();
    const discordId = interaction.user.id;
    
    // Fetch User
    let user = await User.findOne({ discordId });
    if (!user) {
        return interaction.reply({ content: "⚠️ You need to register first! Run `/hyperfocus start` to begin.", ephemeral: true });
    }

    if (subcommand === 'browse') {
        const items = await ShopItem.find({ isActive: true });
        
        if (items.length === 0) {
            return interaction.reply("🏪 The shop is currently empty. Come back later!");
        }

        const embed = new EmbedBuilder()
            .setColor('#2ecc71')
            .setTitle('🏪 Hyper Store')
            .setDescription(`**Your Balance:** ${user.broskiBalance.toFixed(2)} BROski$`)
            .setFooter({ text: 'Use /shop buy <item> to purchase' });

        items.forEach(item => {
            embed.addFields({
                name: `${item.metadata.icon || '📦'} ${item.name} — ${item.price} $`,
                value: item.description,
                inline: false
            });
        });

        return interaction.reply({ embeds: [embed] });
    }

    if (subcommand === 'inventory') {
        // Populate inventory details
        await user.populate('inventory.itemId');
        
        if (user.inventory.length === 0) {
            return interaction.reply({ content: "🎒 Your inventory is empty. Go shopping!", ephemeral: true });
        }

        const embed = new EmbedBuilder()
            .setColor('#3498db')
            .setTitle(`🎒 ${interaction.user.username}'s Inventory`)
            .setDescription('Here is what you own:');

        user.inventory.forEach(slot => {
            if (slot.itemId) {
                embed.addFields({
                    name: `${slot.itemId.metadata?.icon || '📦'} ${slot.itemId.name}`,
                    value: `Purchased: <t:${Math.floor(slot.purchasedAt.getTime()/1000)}:R>`,
                    inline: true
                });
            }
        });

        return interaction.reply({ embeds: [embed] });
    }

    if (subcommand === 'buy') {
        const itemName = interaction.options.getString('item');
        const item = await ShopItem.findOne({ name: itemName });

        if (!item) {
            return interaction.reply({ content: "❌ Item not found.", ephemeral: true });
        }

        // 1. Check Balance
        if (user.broskiBalance < item.price) {
            return interaction.reply({ 
                content: `💸 Insufficient funds! You need **${item.price - user.broskiBalance}** more BROski$.`, 
                ephemeral: true 
            });
        }

        // 2. Check Duplicate (if unique)
        const alreadyOwns = user.inventory.some(slot => slot.itemId && slot.itemId.equals(item._id));
        if (alreadyOwns && item.category !== 'Consumable') {
            return interaction.reply({ content: "⚠️ You already own this item!", ephemeral: true });
        }

        // 3. Process Transaction
        try {
            // Deduct Balance
            user.broskiBalance -= item.price;
            
            // Add to Inventory
            user.inventory.push({
                itemId: item._id,
                purchasedAt: new Date(),
                isEquipped: false
            });

            await user.save();

            // Log Transaction
            await Transaction.create({
                userId: discordId,
                itemId: item._id,
                amount: item.price,
                type: 'Purchase'
            });

            const embed = new EmbedBuilder()
                .setColor('#f1c40f')
                .setTitle('🎉 Purchase Successful!')
                .setDescription(`You bought **${item.name}** for ${item.price} BROski$.`)
                .addFields({ name: 'Remaining Balance', value: `${user.broskiBalance.toFixed(2)} BROski$` });

            return interaction.reply({ embeds: [embed] });

        } catch (error) {
            console.error(error);
            return interaction.reply({ content: "❌ Transaction failed. Please try again.", ephemeral: true });
        }
    }
  },
};

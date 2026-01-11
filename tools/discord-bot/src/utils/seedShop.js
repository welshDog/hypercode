const mongoose = require('mongoose');
const ShopItem = require('../models/ShopItem');
const path = require('path');
require('dotenv').config({ path: path.resolve(__dirname, '../../.env') });

const initialItems = [
  {
    name: 'Neon Night Theme',
    description: 'A cyberpunk aesthetic for your Dashboard.',
    price: 500,
    category: 'Theme',
    metadata: { themeName: 'neon-night', icon: '🌃' }
  },
  {
    name: 'Hyper Legend Role',
    description: 'Exclusive Discord role for the elite.',
    price: 1000,
    category: 'Role',
    metadata: { roleId: 'hyper-legend-id', icon: '👑' }
  },
  {
    name: 'Focus Potion (1h)',
    description: '2x BROski$ earnings for 1 hour.',
    price: 150,
    category: 'Consumable',
    metadata: { durationDays: 0, icon: '🧪' }
  }
];

const seedShop = async () => {
  try {
    if (!process.env.MONGODB_URI) {
        throw new Error("MONGODB_URI is missing in .env");
    }

    await mongoose.connect(process.env.MONGODB_URI);
    console.log('🔌 Connected to MongoDB');

    // Clear existing (optional, but good for dev)
    await ShopItem.deleteMany({});
    console.log('🧹 Cleared existing shop items');

    await ShopItem.insertMany(initialItems);
    console.log('🛍️ Shop stocked with initial items!');

    process.exit(0);
  } catch (error) {
    console.error('❌ Seed Error:', error);
    process.exit(1);
  }
};

seedShop();

const mongoose = require('mongoose');

const shopItemSchema = new mongoose.Schema({
  name: { type: String, required: true, unique: true },
  description: { type: String, required: true },
  price: { type: Number, required: true },
  category: { 
    type: String, 
    enum: ['Role', 'Theme', 'Consumable', 'Special'], 
    default: 'Role' 
  },
  metadata: {
    roleId: String,       // For Discord Roles
    themeName: String,    // For Dashboard Skins
    durationDays: Number, // For temporary items
    icon: String          // Emoji or URL
  },
  isActive: { type: Boolean, default: true },
  createdAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('ShopItem', shopItemSchema);

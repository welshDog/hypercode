const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  discordId: { type: String, required: true, unique: true },
  username: String,
  email: String,
  roles: [String],
  
  // Token Economy
  broskiBalance: { type: Number, default: 0 },
  totalEarned: { type: Number, default: 0 },
  
  // Productivity Tracking
  totalFocusTime: { type: Number, default: 0 }, // in minutes
  currentStreak: { type: Number, default: 0 },
  longestStreak: { type: Number, default: 0 },
  sessionCount: { type: Number, default: 0 },
  
  // Rank & Tier (New)
  rank: { type: String, default: 'Novice' },
  tier: { type: String, enum: ['Free', 'Pro', 'Elite'], default: 'Free' },
  
  // Gamification
  achievements: [String],
  level: { type: Number, default: 1 },
  exp: { type: Number, default: 0 },
  
  // Community
  joinedAt: { type: Date, default: Date.now },
  lastActive: Date,

  // Inventory (Items owned)
  inventory: [{
    itemId: { type: mongoose.Schema.Types.ObjectId, ref: 'ShopItem' },
    purchasedAt: { type: Date, default: Date.now },
    isEquipped: { type: Boolean, default: false }
  }]
});

// Index for leaderboard queries
userSchema.index({ broskiBalance: -1 });
userSchema.index({ currentStreak: -1 });

module.exports = mongoose.model('User', userSchema);

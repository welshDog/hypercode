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
  
  // Gamification
  achievements: [String],
  level: { type: Number, default: 1 },
  exp: { type: Number, default: 0 },
  
  // Community
  joinedAt: { type: Date, default: Date.now },
  lastActive: Date
});

module.exports = mongoose.model('User', userSchema);

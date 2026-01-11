const mongoose = require('mongoose');

const streakSchema = new mongoose.Schema({
  userId: { type: String, required: true, index: true },
  date: { type: Date, required: true }, // Normalized to midnight UTC
  activityCount: { type: Number, default: 0 }, // Number of sessions that day
  totalFocusMinutes: { type: Number, default: 0 },
  tokensEarned: { type: Number, default: 0 },
  
  // Metadata for the calendar visualization
  intensity: { type: Number, default: 0 } // 0-4 scale for heatmap coloring
});

// Compound index to prevent duplicate entries per user per day
streakSchema.index({ userId: 1, date: 1 }, { unique: true });

module.exports = mongoose.model('Streak', streakSchema);

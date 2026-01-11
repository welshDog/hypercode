const mongoose = require('mongoose');

const leaderboardSchema = new mongoose.Schema({
  type: { 
    type: String, 
    enum: ['Daily', 'Weekly', 'Monthly', 'AllTime'],
    required: true 
  },
  date: { type: Date, default: Date.now }, // Snapshot date
  
  // The ranked list
  entries: [{
    userId: String,
    username: String,
    score: Number,
    rank: Number
  }]
});

// Auto-expire daily/weekly snapshots after 90 days to save space
leaderboardSchema.index({ date: 1 }, { expireAfterSeconds: 7776000 });

module.exports = mongoose.model('Leaderboard', leaderboardSchema);

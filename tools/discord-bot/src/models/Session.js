const mongoose = require('mongoose');

const sessionSchema = new mongoose.Schema({
  userId: { type: String, required: true, index: true },
  guildId: String,
  startTime: { type: Date, required: true },
  endTime: Date,
  focusMinutes: Number,
  tasksCompleted: Number,
  earnedTokens: Number,
  githubCommits: { type: Number, default: 0 },
  sessionType: { 
    type: String, 
    enum: ['Coding', 'Design', 'Writing', 'Learning', 'Other'],
    default: 'Coding' 
  },
  notes: String,
  status: { 
    type: String, 
    enum: ['active', 'completed', 'abandoned'], 
    default: 'active' 
  }
});

module.exports = mongoose.model('Session', sessionSchema);

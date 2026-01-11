const mongoose = require('mongoose');

const aiCoachMemorySchema = new mongoose.Schema({
  userId: { type: String, required: true, index: true },
  
  // Context Types
  type: { 
    type: String, 
    enum: ['SessionSummary', 'Goal', 'Blocker', 'Preference', 'AdviceGiven'],
    required: true 
  },
  
  // The actual memory content
  content: { type: String, required: true },
  
  // For vector search relevance (future proofing)
  tags: [String],
  importance: { type: Number, default: 1 }, // 1-5 scale
  
  createdAt: { type: Date, default: Date.now },
  expiresAt: Date // Some memories might be temporary
});

module.exports = mongoose.model('AICoachMemory', aiCoachMemorySchema);

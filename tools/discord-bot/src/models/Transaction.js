const mongoose = require('mongoose');

const transactionSchema = new mongoose.Schema({
  userId: { type: String, required: true, index: true },
  itemId: { type: mongoose.Schema.Types.ObjectId, ref: 'ShopItem', required: true },
  amount: { type: Number, required: true },
  type: { type: String, enum: ['Purchase', 'Refund', 'Gift'], default: 'Purchase' },
  status: { type: String, enum: ['Pending', 'Completed', 'Failed'], default: 'Completed' },
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Transaction', transactionSchema);

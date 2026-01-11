const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');
const User = require('../src/models/User');

let mongoServer;

beforeAll(async () => {
  mongoServer = await MongoMemoryServer.create();
  const uri = mongoServer.getUri();
  await mongoose.connect(uri);
});

afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});

describe('User Model Test', () => {
  it('should create & save user successfully', async () => {
    const validUser = new User({
      discordId: '123456789',
      username: 'TestWarrior',
      broskiBalance: 100
    });
    const savedUser = await validUser.save();
    
    expect(savedUser._id).toBeDefined();
    expect(savedUser.username).toBe('TestWarrior');
    expect(savedUser.broskiBalance).toBe(100);
    expect(savedUser.rank).toBe('Novice'); // Default value check
  });

  it('should fail if discordId is missing', async () => {
    const userWithoutId = new User({ username: 'NoIdUser' });
    let err;
    try {
      await userWithoutId.save();
    } catch (error) {
      err = error;
    }
    expect(err).toBeInstanceOf(mongoose.Error.ValidationError);
  });
});

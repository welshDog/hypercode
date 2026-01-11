module.exports = {
  testEnvironment: 'node',
  verbose: true,
  setupFiles: ['dotenv/config'],
  testTimeout: 10000,
  testMatch: ['**/tests/**/*.test.js'],
};

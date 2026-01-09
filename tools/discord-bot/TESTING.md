# 🧪 BROski Bot Testing Guide

This document outlines the testing protocols for the BROski Discord Bot. We use a custom stress-test suite to simulate Discord interactions and verify token economy logic without needing a live bot token.

## 🏃 Quick Start

Run the stress test suite:

```bash
# Navigate to bot directory
cd tools/discord-bot

# Run the test runner
node tests/stress_test.js
```

**Expected Output:**
```text
🧪 STARTING STRESS TEST...

TEST: Start Session -> Success ... PASSED
TEST: Start Session -> Fail (Duplicate) ... PASSED
TEST: Stop Session -> Success & Math Check (25m = 1 Token) ... PASSED
TEST: Stop Session -> Fail (No Session) ... PASSED
TEST: Math: 50 mins + 0 Streak ... PASSED
TEST: Math: 25 mins + 30 Day Streak (2x Multiplier) ... PASSED

📊 TEST SUMMARY COMPLETE
```

## 🧠 Test Scenarios

### 1. Session Management
- **Start Session**: Verifies that `/hyperfocus start` creates an active session in MongoDB.
- **Duplicate Prevention**: Ensures a user cannot start a second session while one is active.
- **Stop Validation**: Ensures `/hyperfocus stop` fails if no session is active.

### 2. Token Economy (Math Verification)
We rigorously test the **BROski$** calculation logic to prevent inflation/deflation bugs.

**Formula:**
```javascript
Base Tokens = Duration (minutes) / 25
Streak Multiplier = 1 + (Current Streak / 30)
Total = Round(Base * Streak Multiplier)
```

**Test Cases:**
| Case | Duration | Streak | Calculation | Expected Result |
|------|----------|--------|-------------|-----------------|
| **Base** | 25 min | 0 days | `1.0 * 1.0` | **1.00** |
| **Long Session** | 50 min | 0 days | `2.0 * 1.0` | **2.00** |
| **Streak Bonus** | 25 min | 30 days | `1.0 * 2.0` | **2.00** |

## 🛠️ Adding New Tests

1. Open `tests/stress_test.js`.
2. Use the `mockInteraction` helper to simulate a command:
   ```javascript
   const i = mockInteraction("command_name", { option: "value" });
   ```
3. Execute the command:
   ```javascript
   await command.execute(i);
   ```
4. Assert the state using the mock DB:
   ```javascript
   const user = await User.findOne({ discordId: "..." });
   assert.equal(user.balance, expectedValue);
   ```

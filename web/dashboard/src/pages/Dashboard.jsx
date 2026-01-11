import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Play, Square, Timer, Zap, Wallet, Activity } from 'lucide-react';
import axios from 'axios';
import Layout from '../components/Layout';
import StreakCalendar from '../components/StreakCalendar';

export default function Dashboard() {
  const [timeLeft, setTimeLeft] = useState(25 * 60);
  const [isActive, setIsActive] = useState(false);
  const [stats, setStats] = useState({ balance: 0, streak: 0, rank: 0, totalEarned: 0 });
  const [sessionType, setSessionType] = useState('Coding');

  const user = JSON.parse(localStorage.getItem('hyper_user') || '{}');
  const USER_ID = user.id; // Get ID from logged in user

  useEffect(() => {
    if (!USER_ID) return;

    const fetchStats = async () => {
      try {
        const res = await axios.get(`http://localhost:3001/api/stats/${USER_ID}`);
        setStats(res.data);
      } catch (err) {
        console.error("Failed to fetch stats", err);
        // Fallback Mock Data handled by API now, but just in case:
        setStats({ balance: 0, streak: 0, rank: 0, totalEarned: 0 });
      }
    };

    fetchStats();
    const poll = setInterval(fetchStats, 10000); // Poll every 10s
    return () => clearInterval(poll);
  }, [USER_ID]);

  // Timer Logic
  useEffect(() => {
    let interval = null;
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => setTimeLeft((t) => t - 1), 1000);
    } else if (timeLeft === 0) {
      setIsActive(false);
      // Play sound or notify
    }
    return () => clearInterval(interval);
  }, [isActive, timeLeft]);

  const toggleTimer = () => setIsActive(!isActive);
  const resetTimer = () => {
    setIsActive(false);
    setTimeLeft(25 * 60);
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  return (
    <Layout>
      {/* Header */}
      <header className="mb-12 flex justify-between items-end">
        <div>
          <h1 className="text-4xl font-bold mb-2">
            Welcome back, <span className="text-hyper-accent">{user.username || 'Commander'}</span>
          </h1>
          <p className="text-gray-400">Ready to enter the flow state?</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-500">Global Rank</div>
          <div className="text-3xl font-bold font-mono">#{stats.rank > 0 ? stats.rank : '-'}</div>
        </div>
      </header>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Col: Timer */}
        <div className="lg:col-span-2 space-y-8">
          <div className="bg-hyper-card p-8 rounded-2xl border border-gray-800 shadow-2xl relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Timer className="w-48 h-48" />
            </div>

            <div className="relative z-10 flex flex-col items-center justify-center py-12">
              <div className="text-8xl font-mono font-bold tracking-tighter mb-8 text-white drop-shadow-[0_0_15px_rgba(0,255,255,0.3)]">
                {formatTime(timeLeft)}
              </div>

              <div className="flex gap-4">
                <button
                  onClick={toggleTimer}
                  className={`px-8 py-4 rounded-xl font-bold text-xl flex items-center gap-2 transition-all ${isActive
                      ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30 border border-red-500/50'
                      : 'bg-hyper-accent text-black hover:bg-cyan-300 shadow-[0_0_20px_rgba(0,255,255,0.4)]'
                    }`}
                >
                  {isActive ? <><Square className="fill-current" /> PAUSE</> : <><Play className="fill-current" /> FOCUS</>}
                </button>
                <button
                  onClick={resetTimer}
                  className="px-6 py-4 rounded-xl font-bold text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
                >
                  RESET
                </button>
              </div>
            </div>
          </div>

          {/* Activity / Calendar */}
          <StreakCalendar streak={stats.streak} />
        </div>

        {/* Right Col: Stats */}
        <div className="space-y-6">
          {/* Balance Card */}
          <motion.div
            whileHover={{ y: -5 }}
            className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800"
          >
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 bg-purple-500/20 rounded-lg text-purple-400">
                <Wallet className="w-6 h-6" />
              </div>
              <div className="text-gray-400">Wallet Balance</div>
            </div>
            <div className="text-4xl font-bold font-mono">{stats.balance} <span className="text-sm text-gray-600">BRO$</span></div>
          </motion.div>

          {/* Streak Card */}
          <motion.div
            whileHover={{ y: -5 }}
            className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800"
          >
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 bg-orange-500/20 rounded-lg text-orange-400">
                <Zap className="w-6 h-6" />
              </div>
              <div className="text-gray-400">Current Streak</div>
            </div>
            <div className="text-4xl font-bold font-mono text-orange-400">{stats.streak} <span className="text-sm text-gray-600">DAYS</span></div>
          </motion.div>

          {/* Total Earned */}
          <motion.div
            whileHover={{ y: -5 }}
            className="bg-gray-900/50 p-6 rounded-2xl border border-gray-800"
          >
            <div className="flex items-center gap-4 mb-2">
              <div className="p-3 bg-green-500/20 rounded-lg text-green-400">
                <Activity className="w-6 h-6" />
              </div>
              <div className="text-gray-400">Lifetime Earned</div>
            </div>
            <div className="text-4xl font-bold font-mono">{stats.totalEarned} <span className="text-sm text-gray-600">BRO$</span></div>
          </motion.div>

        </div>
      </div>
    </Layout>
  );
}
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Trophy, Medal, Zap } from 'lucide-react';
import Layout from '../components/Layout';
import axios from 'axios';

export default function Leaderboard() {
  const [leaders, setLeaders] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        const res = await axios.get('http://localhost:3001/api/leaderboard');
        setLeaders(res.data);
      } catch (err) {
        console.error("Failed to fetch leaderboard", err);
        // Fallback Mock Data
        setLeaders([
            { discordId: '1', username: 'NeonRunner', balance: 5000, streak: 42 },
            { discordId: '2', username: 'CyberMonk', balance: 4200, streak: 30 },
            { discordId: '3', username: 'GlitchWitch', balance: 3800, streak: 15 },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchLeaderboard();
  }, []);

  const getRankIcon = (index) => {
    if (index === 0) return <Trophy className="w-8 h-8 text-yellow-400" />;
    if (index === 1) return <Medal className="w-8 h-8 text-gray-400" />;
    if (index === 2) return <Medal className="w-8 h-8 text-amber-600" />;
    return <span className="text-xl font-bold text-gray-500">#{index + 1}</span>;
  };

  return (
    <Layout>
      <header className="mb-12">
        <h1 className="text-4xl font-bold mb-2 flex items-center gap-4">
            <Trophy className="text-yellow-400 w-10 h-10" />
            Global <span className="text-hyper-accent">Leaderboard</span>
        </h1>
        <p className="text-gray-400">Top Hyperfocus Commanders</p>
      </header>

      <div className="bg-hyper-card rounded-2xl border border-gray-800 overflow-hidden">
        {loading ? (
            <div className="p-12 text-center text-gray-500 animate-pulse">Syncing Neural Network...</div>
        ) : (
            <table className="w-full text-left">
                <thead className="bg-gray-800/50 text-gray-400">
                    <tr>
                        <th className="p-6">Rank</th>
                        <th className="p-6">Commander</th>
                        <th className="p-6 text-right">Balance</th>
                        <th className="p-6 text-right">Streak</th>
                    </tr>
                </thead>
                <tbody>
                    {leaders.map((user, index) => (
                        <motion.tr 
                            key={user.discordId}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            className="border-b border-gray-800 hover:bg-gray-800/30 transition-colors"
                        >
                            <td className="p-6 w-24">{getRankIcon(index)}</td>
                            <td className="p-6 font-bold text-lg">{user.username}</td>
                            <td className="p-6 text-right font-mono text-hyper-accent">
                                {user.balance} <span className="text-xs text-gray-500">BRO$</span>
                            </td>
                            <td className="p-6 text-right flex justify-end items-center gap-2">
                                <Zap className="w-4 h-4 text-orange-500" /> {user.streak}
                            </td>
                        </motion.tr>
                    ))}
                </tbody>
            </table>
        )}
      </div>
    </Layout>
  );
}

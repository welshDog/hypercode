import { motion } from 'framer-motion';
import { LogIn } from 'lucide-react';
import axios from 'axios';

export default function Login() {

  const handleLogin = async () => {
    try {
      // 1. Get Auth URL from Bot
      const res = await axios.get('http://localhost:3001/api/auth/login');
      if (res.data.url) {
        window.location.href = res.data.url;
      }
    } catch (err) {
      console.error("Login Failed", err);
      alert("Bot API offline or configured incorrectly.");
    }
  };

  return (
    <div className="h-screen w-screen bg-hyper-dark text-hyper-text flex items-center justify-center relative overflow-hidden">
      {/* Background Ambience */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-violet-900/20 via-hyper-dark to-hyper-dark" />
      
      <div className="z-10 text-center space-y-8 p-8">
        <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5 }}
        >
            <h1 className="text-6xl font-black tracking-tighter mb-2">
                HYPER<span className="text-hyper-accent">CODE</span>
            </h1>
            <p className="text-xl text-gray-400">The Neural Interface for Flow State</p>
        </motion.div>

        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleLogin}
            className="flex items-center gap-3 bg-[#5865F2] hover:bg-[#4752C4] text-white px-8 py-4 rounded-xl font-bold text-xl shadow-lg shadow-violet-900/50 mx-auto transition-all"
        >
            <LogIn className="w-6 h-6" />
            Initialize Neural Link
        </motion.button>
        
        <p className="text-sm text-gray-500 mt-4">Powered by Discord OAuth</p>
      </div>
    </div>
  );
}

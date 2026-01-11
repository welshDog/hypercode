import { Zap, LayoutDashboard, Trophy, LogOut } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

export default function Navbar() {
  const location = useLocation();
  const isActive = (path) => location.pathname === path ? "text-hyper-accent" : "text-gray-400 hover:text-white";

  return (
    <nav className="fixed top-0 left-0 h-screen w-20 bg-hyper-card flex flex-col items-center py-8 border-r border-gray-800">
      <div className="mb-12">
        <Zap className="w-8 h-8 text-hyper-accent animate-pulse" />
      </div>
      
      <div className="flex flex-col gap-8 flex-1">
        <Link to="/" className={isActive('/')}>
          <LayoutDashboard className="w-6 h-6" />
        </Link>
        <Link to="/leaderboard" className={isActive('/leaderboard')}>
          <Trophy className="w-6 h-6" />
        </Link>
      </div>

      <button className="text-gray-400 hover:text-red-400">
        <LogOut className="w-6 h-6" />
      </button>
    </nav>
  );
}
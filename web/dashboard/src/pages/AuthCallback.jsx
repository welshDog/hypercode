import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import axios from 'axios';
import { Loader2 } from 'lucide-react';

export default function AuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [status, setStatus] = useState("Establishing Secure Link...");

  useEffect(() => {
    const code = searchParams.get('code');
    
    if (!code) {
        navigate('/login');
        return;
    }

    const exchangeCode = async () => {
        try {
            setStatus("Handshaking with Neural Core...");
            const res = await axios.post('http://localhost:3001/api/auth/exchange', { code });
            
            if (res.data.user) {
                setStatus("Access Granted.");
                localStorage.setItem('hyper_user', JSON.stringify(res.data.user));
                localStorage.setItem('hyper_token', res.data.token);
                
                // Small delay for effect
                setTimeout(() => navigate('/'), 1000);
            }
        } catch (err) {
            console.error("Auth Failed", err);
            setStatus("Link Failed. Retrying...");
            setTimeout(() => navigate('/login'), 2000);
        }
    };

    exchangeCode();
  }, [searchParams, navigate]);

  return (
    <div className="h-screen w-screen bg-hyper-dark text-hyper-text flex flex-col items-center justify-center gap-4">
      <Loader2 className="w-12 h-12 text-hyper-accent animate-spin" />
      <h2 className="text-2xl font-mono text-hyper-accent animate-pulse">{status}</h2>
    </div>
  );
}

import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Shield, Activity, AlertTriangle } from 'lucide-react';
import io from 'socket.io-client';

const socket = io("http://127.0.0.1:5000");

function App() {
  const [data, setData] = useState([]);
  const [status, setStatus] = useState("NORMAL");
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    socket.on("connect", () => setConnected(true));
    socket.on("packet", (payload) => {
      setStatus(payload.status);
      setData(prev => [...prev.slice(-19), { 
        time: new Date().toLocaleTimeString(), 
        val: payload.status === "NORMAL" ? 1 : 2 
      }]);
    });
    return () => socket.off("packet");
  }, []);

  return (
    <div style={{ backgroundColor: '#0f172a', color: 'white', minHeight: '100vh', padding: '20px', fontFamily: 'sans-serif' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '30px' }}>
        <h1 style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <Shield color="#38bdf8" /> SOC AI Monitoring Dashboard
        </h1>
        <div style={{ padding: '10px', borderRadius: '8px', backgroundColor: connected ? '#065f46' : '#991b1b' }}>
          {connected ? "● BACKEND CONNECTED" : "○ DISCONNECTED"}
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px' }}>
        <div style={{ padding: '20px', borderRadius: '12px', backgroundColor: '#1e293b', textAlign: 'center' }}>
          <h3>Current System Status</h3>
          <h2 style={{ color: status === "NORMAL" ? "#4ade80" : "#f87171", fontSize: '3rem' }}>
            {status}
          </h2>
        </div>
        <div style={{ padding: '20px', borderRadius: '12px', backgroundColor: '#1e293b' }}>
          <h3>Live Threat Level</h3>
          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
              <XAxis dataKey="time" hide />
              <YAxis domain={[0, 3]} hide />
              <Tooltip />
              <Line type="monotone" dataKey="val" stroke="#38bdf8" strokeWidth={3} dot={false} isAnimationActive={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;
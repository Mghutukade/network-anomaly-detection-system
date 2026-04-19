import React, { useState, useEffect } from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { ShieldAlert, Terminal, Activity, Zap, ShieldCheck } from 'lucide-react';
import io from 'socket.io-client';
import './App.css';

const socket = io("http://127.0.0.1:5000");

function App() {
  const [data, setData] = useState([]);
  const [logs, setLogs] = useState([]);
  const [status, setStatus] = useState("SECURE");

  useEffect(() => {
    socket.on("packet", (payload) => {
      const time = new Date().toLocaleTimeString();
      setStatus(payload.status);
      
      // Update Waveform
      setData(prev => [...prev.slice(-20), { 
        time, 
        val: payload.status === "NORMAL" ? 15 + Math.random()*10 : 90 
      }]);

      // NEW: Tactical IP Logging
      const logEntry = {
        id: Date.now(),
        time: time,
        src: payload.src_ip,
        dst: payload.dst_ip,
        proto: payload.protocol,
        threat: payload.threat_level,
        status: payload.status
      };
      
      setLogs(prev => [logEntry, ...prev.slice(0, 12)]);
    });
    return () => socket.off("packet");
  }, []);

  return (
    <div className={`app-container ${status !== "NORMAL" ? "alert-mode" : ""}`}>
      <header className="tactical-header">
        <div className="title-section">
          <ShieldAlert size={28} className={status !== "NORMAL" ? "icon-alert" : ""} />
          <h1>NADS // INTEL_COMMAND_CENTER</h1>
        </div>
        <div className="header-stats">
          <span className="location-tag">[MUMBAI_HQ]</span>
          <span className="uplink">● UPLINK_ACTIVE</span>
        </div>
      </header>

      <div className="dashboard-grid">
        {/* Left Side: Visual Analysis */}
        <div className="visual-section">
          <div className="chart-container">
            <h3><Activity size={16} /> NETWORK_TRAFFIC_WAVEFORM</h3>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={data}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                <XAxis dataKey="time" hide />
                <YAxis domain={[0, 100]} hide />
                <Area 
                  type="stepAfter" 
                  dataKey="val" 
                  stroke={status === "NORMAL" ? "#38bdf8" : "#ef4444"} 
                  fill={status === "NORMAL" ? "rgba(56, 189, 248, 0.2)" : "rgba(239, 68, 68, 0.4)"} 
                  isAnimationActive={false}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="status-grid">
            <div className={`stat-card ${status !== "NORMAL" ? "danger" : ""}`}>
              <span className="label">CURRENT_THREAT</span>
              <span className="value">{status}</span>
            </div>
            <div className="stat-card">
              <span className="label">ENCRYPTION</span>
              <span className="value">AES_256</span>
            </div>
          </div>
        </div>

        {/* Right Side: IP Intel Feed */}
        <div className="feed-section">
          <h3><Terminal size={16} /> LIVE_IP_INTERCEPT_FEED</h3>
          <div className="terminal-window">
            <div className="terminal-header">
              <span>TIMESTAMP</span>
              <span>SOURCE_IP</span>
              <span>PROTOCOL</span>
              <span>THREAT</span>
            </div>
            <div className="terminal-body">
              {logs.map((log) => (
                <div key={log.id} className={`log-row ${log.status !== 'NORMAL' ? 'row-alert' : ''}`}>
                  <span>{log.time}</span>
                  <span className="ip-addr">{log.src}</span>
                  <span>{log.proto}</span>
                  <span className="threat-val">{log.threat}%</span>
                </div>
              ))}
              <div className="cursor">_ SCANNING_NETWORK...</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
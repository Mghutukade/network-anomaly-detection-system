import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import './App.css';

// Ensure this matches your Flask server address
const socket = io("http://127.0.0.1:5000");

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [stream, setStream] = useState([]);
  const [graphData, setGraphData] = useState([]);
  const [risk, setRisk] = useState(0);
  const [time, setTime] = useState(new Date().toLocaleTimeString());
  const [stats, setStats] = useState({ total: 0, critical: 0, avgRisk: 0 });

  useEffect(() => {
    const clock = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    
    socket.on("intel_stream", (data) => {
      if (isLoggedIn) {
        // Update Live Table (keep last 15 packets)
        setStream(prev => [data, ...prev].slice(0, 15));
        
        // Update Global Risk Gauge
        setRisk(data.threat);
        
        // Update Entropy Graph Data
        setGraphData(prev => [...prev.slice(-30), { 
          t: data.timestamp, 
          v: data.threat, 
          e: data.entropy 
        }]);
        
        // Update Executive Metrics
        setStats(prev => ({
          total: prev.total + 1,
          critical: data.threat > 80 ? prev.critical + 1 : prev.critical,
          avgRisk: Math.floor(((prev.avgRisk * prev.total) + data.threat) / (prev.total + 1))
        }));
      }
    });

    return () => {
      clearInterval(clock);
      socket.off("intel_stream");
    };
  }, [isLoggedIn]);

  const handleLogin = async () => {
    try {
      const res = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp })
      });
      const result = await res.json();
      if (result.status === 'success') setIsLoggedIn(true);
      else alert("ACCESS_DENIED: UNAUTHORIZED CREDENTIALS");
    } catch (err) {
      alert("SERVER_OFFLINE: CHECK FLASK TERMINAL");
    }
  };

  if (!isLoggedIn) {
    return (
      <div className="auth-screen">
        <div className="auth-box">
          <div className="auth-header">
            <h2>NADS_SECURE_KERNEL</h2>
            <p>ADMIN_LEVEL_AUTHENTICATION_v2.5</p>
          </div>
          <input placeholder="ADMIN_EMAIL" onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="ADMIN_PASSWORD" onChange={e => setPassword(e.target.value)} />
          <button className="otp-btn" onClick={() => fetch('http://localhost:5000/generate-otp', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          })}>REQUEST_SECURITY_TOKEN</button>
          <input placeholder="ENTER_OTP" onChange={e => setOtp(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>AUTHORIZE_SESSION</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="header">
        <div className="brand">
          <div className="pulse-icon"></div>
          <h1>NADS // ENTERPRISE_FORENSICS_v2.5</h1>
        </div>
        <div className="stats-bar">
          <div className="stat-item">
            <span className="label">TOTAL_SCANS</span>
            <span className="value">{stats.total}</span>
          </div>
          <div className="stat-item danger-text">
            <span className="label">CRITICAL_THREATS</span>
            <span className="value">{stats.critical}</span>
          </div>
          <div className="stat-item">
            <span className="label">AVG_RISK</span>
            <span className="value">{stats.avgRisk}%</span>
          </div>
          <div className="timer-box">{time}</div>
        </div>
      </header>

      <div className="main-layout">
        <aside className="risk-sidebar">
          {/* Risk Gauge Module */}
          <div className="module-card">
            <div className="module-label">LIVE_THREAT_INDEX</div>
            <div className={`big-gauge ${risk > 80 ? 'critical' : ''}`}>
              {risk}<span>%</span>
            </div>
            <p className="risk-desc">{risk > 80 ? "ALERT: ANOMALY DETECTED" : "STATUS: NORMAL_TRAFFIC"}</p>
          </div>

          {/* Entropy Pattern Module (UPGRADED WITH AREA CHART) */}
          <div className="module-card">
            <div className="module-label">ENTROPY_PATTERN_TRACKER</div>
            <ResponsiveContainer width="100%" height={160}>
              <AreaChart data={graphData}>
                <defs>
                  <linearGradient id="colorThreat" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor={risk > 80 ? "#ff003c" : "#00f3ff"} stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#010103" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="1 4" stroke="#00414a" vertical={false}/>
                <Tooltip 
                  contentStyle={{backgroundColor: '#000', border: '1px solid #00f3ff', color: '#00f3ff', fontSize: '10px'}}
                />
                <Area 
                  type="stepAfter" 
                  dataKey="v" 
                  stroke={risk > 80 ? "#ff003c" : "#00f3ff"} 
                  fillOpacity={1} 
                  fill="url(#colorThreat)" 
                  isAnimationActive={false} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </aside>

        {/* Real-Time Table Section */}
        <section className="forensics-container">
          <div className="table-header">
            <div className="module-label">REAL-TIME_TRAFFIC_FORENSICS</div>
            <div className="db-status">POSTGRESQL_SYNC: ACTIVE</div>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>SOURCE_ORIGIN</th>
                  <th>ATTACK_VECTOR</th>
                  <th>NODE_TARGET</th>
                  <th>RISK</th>
                  <th>ACTION_STATUS</th>
                </tr>
              </thead>
              <tbody>
                {stream.map((p, i) => (
                  <tr key={i} className={p.threat > 80 ? 'high-threat-row' : ''}>
                    <td className="mono">
                      <span className="ip-cell">{p.src}</span>
                      <div className="sub-label">PORT: {p.port || 'DYNAMIC'}</div>
                    </td>
                    <td><span className="vector-tag">{p.vector}</span></td>
                    <td className="mono" style={{opacity: 0.7}}>{p.dest}</td>
                    <td className={p.threat > 80 ? 'risk-high' : 'risk-low'}>{p.threat}%</td>
                    <td>
                      <span className={`status-badge ${p.threat > 80 ? 'blocked' : 'monitored'}`}>
                        {p.threat > 80 ? "ARCHIVED" : "MONITORING"}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;
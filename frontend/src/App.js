import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { LineChart, Line, ResponsiveContainer, YAxis, CartesianGrid, Tooltip } from 'recharts';
import './App.css';

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
        setStream(prev => [data, ...prev].slice(0, 15));
        setRisk(data.threat);
        // Use 'v' for threat and 'e' for entropy tracking
        setGraphData(prev => [...prev.slice(-25), { t: data.timestamp, v: data.threat, e: data.entropy }]);
        
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
    const res = await fetch('http://localhost:5000/login', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, otp })
    });
    const result = await res.json();
    if (result.status === 'success') setIsLoggedIn(true);
    else alert("ACCESS_DENIED: UNAUTHORIZED");
  };

  if (!isLoggedIn) {
    return (
      <div className="auth-screen">
        <div className="auth-box">
          <div className="auth-header">
            <h2>NADS_SECURE_KERNEL</h2>
            <p>AUTHORIZED_ACCESS_ONLY</p>
          </div>
          <input placeholder="ADMIN_ID" onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="SECRET_KEY" onChange={e => setPassword(e.target.value)} />
          <button className="otp-btn" onClick={() => fetch('http://localhost:5000/generate-otp', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
          })}>GET_AUTH_TOKEN</button>
          <input placeholder="UNIQUE_OTP" onChange={e => setOtp(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>VERIFY_&_ENTER</button>
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
          <div className="module-card">
            <div className="module-label">LIVE_THREAT_INDEX</div>
            <div className={`big-gauge ${risk > 80 ? 'critical' : ''}`}>
              {risk}<span>%</span>
            </div>
            <p className="risk-desc">{risk > 80 ? "!!! ALERT: ANOMALY !!!" : "SYSTEM: STABLE"}</p>
          </div>

          <div className="module-card tracker">
            <div className="module-label">ENTROPY_PATTERN_TRACKER</div>
            <ResponsiveContainer width="100%" height={160}>
              <LineChart data={graphData}>
                <CartesianGrid strokeDasharray="1 4" stroke="#00414a" vertical={false}/>
                <Tooltip 
                  contentStyle={{backgroundColor: '#000', border: '1px solid #00f3ff', fontSize: '10px'}}
                  itemStyle={{color: '#00f3ff'}}
                />
                <Line 
                  type="stepAfter" 
                  dataKey="v" 
                  stroke={risk > 80 ? "#ff003c" : "#00f3ff"} 
                  strokeWidth={2} 
                  dot={{ r: 2, fill: '#00f3ff' }} 
                  isAnimationActive={false} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </aside>

        <section className="forensics-container">
          <div className="table-header">
            <div className="module-label">REAL-TIME_ANOMALY_FORENSICS</div>
            <div className="db-status">POSTGRES_SYNC: ACTIVE</div>
          </div>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ORIGIN</th>
                  <th>VECTOR</th>
                  <th>NODE_TARGET</th>
                  <th>THREAT</th>
                  <th>ACTION</th>
                </tr>
              </thead>
              <tbody>
                {stream.map((p, i) => (
                  <tr key={i} className={p.threat > 80 ? 'high-threat-row' : ''}>
                    <td className="ip-cell mono">{p.src}</td>
                    <td><span className="vector-tag">{p.vector}</span></td>
                    <td className="mono" style={{opacity: 0.6}}>{p.dest}</td>
                    <td className={p.threat > 80 ? 'risk-high' : 'risk-low'}>{p.threat}%</td>
                    <td>
                      <span className={`status-badge ${p.threat > 80 ? 'blocked' : 'monitored'}`}>
                        {p.threat > 80 ? "ARCHIVED" : "MONITOR"}
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
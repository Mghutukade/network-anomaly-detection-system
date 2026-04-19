import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import { LineChart, Line, ResponsiveContainer } from 'recharts';
import './App.css';

const socket = io("http://127.0.0.1:5000");

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState(''); // New State
  const [otp, setOtp] = useState('');
  const [stream, setStream] = useState([]);
  const [graphData, setGraphData] = useState([]);
  const [risk, setRisk] = useState(0);
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const clock = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    socket.on("intel_stream", (data) => {
      if (isLoggedIn) {
        setStream(prev => [data, ...prev].slice(0, 12));
        setRisk(data.threat);
        setGraphData(prev => [...prev.slice(-30), {t: data.timestamp, v: data.threat}]);
      }
    });
    return () => clearInterval(clock);
  }, [isLoggedIn]);

  const handleLogin = async () => {
    const res = await fetch('http://localhost:5000/login', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ email, otp })
    });
    const result = await res.json();
    if (result.status === 'success') setIsLoggedIn(true);
    else alert("AUTH_FAILED");
  };

  if (!isLoggedIn) {
    return (
      <div className="auth-screen">
        <div className="auth-box">
          <h2>NETWORK_ANOMALY_DETECTION</h2>
          <input placeholder="ADMIN_EMAIL" onChange={e => setEmail(e.target.value)} />
          <input type="password" placeholder="ADMIN_PASSWORD" onChange={e => setPassword(e.target.value)} />
          <button onClick={() => fetch('http://localhost:5000/generate-otp', {
            method:'POST', 
            headers:{'Content-Type':'application/json'}, 
            body:JSON.stringify({email, password}) // Send password for OTP
          })}>REQUEST_OTP</button>
          <input placeholder="ENTER_OTP" onChange={e => setOtp(e.target.value)} />
          <button className="login-btn" onClick={handleLogin}>AUTHORIZE_LOGIN</button>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>NETWORK ANOMALY DETECTION SYSTEM</h1>
        <div className="top-right"><span>{time}</span></div>
      </header>
      <div className="main-layout">
        <div className="risk-sidebar">
          <div className="gauge-label">24/7_RISK_SCORE</div>
          <div className={`gauge ${risk > 80 ? 'danger' : ''}`}>{risk}%</div>
          <ResponsiveContainer width="100%" height={100}>
            <LineChart data={graphData}><Line type="monotone" dataKey="v" stroke="#00f3ff" dot={false} isAnimationActive={false}/></LineChart>
          </ResponsiveContainer>
        </div>
        <div className="flow-table">
          <table>
            <thead><tr><th>SOURCE</th><th>VECTOR</th><th>DESTINATION</th><th>RISK</th></tr></thead>
            <tbody>
              {stream.map((p, i) => (
                <tr key={i}>
                  <td>{p.src}</td><td>▶▶▶</td><td>{p.dest}</td>
                  <td style={{color: p.threat > 80 ? 'red' : '#00ff9d'}}>{p.threat}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
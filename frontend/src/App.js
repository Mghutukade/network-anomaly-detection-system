import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import { AreaChart, Area, ResponsiveContainer, YAxis, CartesianGrid } from 'recharts';
import './App.css';

const socket = io("http://127.0.0.1:5000");

function App() {
  const [stream, setStream] = useState([]);
  const [graphData, setGraphData] = useState([]);
  const [packetCount, setPacketCount] = useState(0); // For that "Aura" math
  const [bitrate, setBitrate] = useState(0);

  useEffect(() => {
    socket.on("intel_stream", (payload) => {
      // 1. Increase display limit to 15 for better "scroll" feel
      setStream(prev => [payload, ...prev].slice(0, 15));
      
      // 2. Aura Math: Calculate cumulative "Network Pressure"
      setPacketCount(prev => prev + 1);
      
      // 3. Graph Logic: Using Hex Size and Entropy for the Waveform
      const hexToInt = parseInt(payload.hex_size, 16);
      const intensity = (hexToInt * payload.entropy) / 100;
      
      setGraphData(prev => [...prev.slice(-30), { 
        time: payload.timestamp, 
        val: intensity,
        threat: payload.threat 
      }]);
    });

    return () => socket.off("intel_stream");
  }, []);

  return (
    <div className="interface">
      <div className="scanner-line"></div>
      
      <header className="top-bar">
        <div className="glitch-header">NADS // FORENSIC_DPI_ENGINE</div>
        <div className="sys-metrics">
          <span>PACKETS_ANALYZED: {packetCount.toLocaleString()}</span>
          <span className="uplink-status">● KERNEL_UPLINK: ACTIVE</span>
        </div>
      </header>

      <div className="forensic-grid">
        {/* WAVEFORM PANEL */}
        <div className="visual-panel">
          <div className="panel-label">HEURISTIC_FLUX_DENSITY</div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={graphData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#001a1d" vertical={false} />
              <YAxis hide domain={[0, 'auto']} />
              <Area 
                type="stepAfter" 
                dataKey="val" 
                stroke="#00f3ff" 
                fill="rgba(0, 243, 255, 0.1)" 
                isAnimationActive={false} // CRITICAL: Set to false for high-speed feeds
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* DATA FEED PANEL */}
        <div className="intel-section">
          <div className="panel-label">> RAW_PACKET_INTERCEPT_STREAM</div>
          <table className="intel-table">
            <thead>
              <tr>
                <th>TIME</th>
                <th>SOURCE_NODE</th>
                <th>VECTOR</th>
                <th>ENTROPY</th>
                <th>SIZE_HEX</th>
                <th>THREAT</th>
              </tr>
            </thead>
            <tbody>
              {stream.map((log, i) => (
                <tr key={i} className={log.threat > 85 ? 'alert-row' : ''}>
                  <td className="dim-txt">{log.timestamp}</td>
                  <td className="cyan-txt">{log.src_ip}</td>
                  <td className="vector-tag">{log.vector}</td>
                  <td>{log.entropy.toFixed(2)}</td>
                  <td className="dim-txt">{log.hex_size}</td>
                  <td className="threat-cell" style={{color: log.threat > 80 ? '#ff003c' : '#00ff9d'}}>
                    {log.threat}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <footer className="footer">
        <div className="cmd-line">
          <span className="prompt">ROOT@NADS_SERVER:~#</span> 
          <span className="typing"> MONITORING_THREADS_ACTIVE... PACKET_BUFFER_OK...</span>
        </div>
      </footer>
    </div>
  );
}

export default App;
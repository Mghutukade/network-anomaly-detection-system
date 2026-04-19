import sys
import os
import time
import threading
import random
import warnings
from flask import Flask
from flask_socketio import SocketIO

# 1. CLEAN TERMINAL: Suppress the Eventlet/Deprecation warnings for the Viva
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 2. SYSTEM BRIDGE: Force Python to find the main.py in the root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 3. INTELLIGENCE LINKING
try:
    # Try importing your actual ML/Sniffer logic
    import main 
    if hasattr(main, 'sniff_packet'):
        sniff_packet = main.sniff_packet
        print("✅ [SUCCESS] INTELLIGENCE LINK ESTABLISHED: main.py connected.")
    else:
        print("⚠️ [WARNING] main.py found, but 'sniff_packet' function is missing.")
        raise AttributeError
except (ImportError, AttributeError):
    print("⚠️ [FALLBACK] LINKING FAILED. Enabling Forensic Simulation Mode.")
    # This fallback ensures you have a working demo even if main.py has an error
    def sniff_packet():
        return {
            'ip': f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(1,255)}",
            'size': random.randint(64, 1500),
            'threat': random.randint(0, 100),
            'entropy': round(random.uniform(2.5, 8.0), 2),
            'flags': f"{random.choice(['SYN', 'ACK', 'FIN'])}|{random.choice(['PSH', 'URG'])}"
        }

# 4. TACTICAL LOGIC
def get_vector(threat_level):
    if threat_level < 25: return "STABLE_ENCLAVE"
    if threat_level < 55: return "HEURISTIC_FLAG"
    if threat_level < 85: return "LATERAL_TRAVERSAL"
    return "ACTIVE_EXPLOIT"

def background_sniffer():
    print("⚡ [CORE] FORENSIC KERNEL ONLINE. MONITORING DATA LINK LAYER...")
    while True:
        try:
            # Get real data from your AI engine
            raw_data = sniff_packet()
            
            threat = raw_data.get('threat', 0)
            
            # Construct high-density forensic payload
            intel_payload = {
                'timestamp': time.strftime('%H:%M:%S'),
                'src_ip': raw_data.get('ip', '0.0.0.0'),
                'vector': get_vector(threat),
                'threat': threat,
                'hex_size': hex(raw_data.get('size', 0)).upper(),
                'entropy': raw_data.get('entropy', 0),
                'flags': raw_data.get('flags', 'NONE'),
                'status': "CRITICAL" if threat > 85 else "ACTIVE"
            }
            
            # Broadcast to React Dashboard
            socketio.emit('intel_stream', intel_payload)
            
        except Exception as e:
            print(f"❌ [KERNEL ERROR]: {e}")
            
        time.sleep(0.4) # Maintains a fast, aggressive scrolling feel

# 5. EXECUTION
if __name__ == '__main__':
    # Run the sniffer in a separate thread so it doesn't block the web server
    threading.Thread(target=background_sniffer, daemon=True).start()
    
    print("📡 [SERVER] DASHBOARD UPLINK PORT: 5000")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
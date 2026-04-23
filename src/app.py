import sys, os, time, threading, random, secrets, warnings
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import psycopg2 

# --- DATABASE CONFIG ---
DB_CONFIG = {
    "dbname": "nads_db",
    "user": "postgres",
    "password": "maheshG39", 
    "host": "localhost",
    "port": "5432"
}

# --- SENSITIVE ADMIN ACCESS ---
ADMIN_DATABASE = {
    "admin@nads.com": "root@2026",
    "vaibhav@nads.com": "titan_secure"
}

# --- DATABASE LOGIC ---
def save_to_forensics(data):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = """
            INSERT INTO forensic_archive (source_node, vector_type, threat_score, entropy_level)
            VALUES (%s, %s, %s, %s)
        """
        cur.execute(query, (data['src'], data['vector'], data['threat'], data['entropy']))
        conn.commit()
        cur.close()
        conn.close()
        print(f"💾 [DATABASE] Forensic log saved: {data['threat']}%")
    except Exception as e:
        print(f"❌ [DB_ERROR]: {e}")

# --- KERNEL SETUP ---
warnings.filterwarnings("ignore", category=DeprecationWarning)
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

active_sessions = {}

# --- INTELLIGENCE LINKING (Sniffer vs Fallback) ---
try:
    import main 
    sniff_logic = main.sniff_packet
    print("✅ [SUCCESS] INTELLIGENCE LINK ESTABLISHED.")
except:
    print("⚠️ [FALLBACK] SIMULATION MODE ACTIVE.")
    def sniff_logic():
        return {
            'ip': f"103.21.{random.randint(1,255)}.{random.randint(1,255)}",
            'size': random.randint(64, 1500),
            'threat': random.randint(0, 100),
            'entropy': round(random.uniform(2.5, 8.0), 2)
        }

# --- AUTH ROUTES ---
@app.route('/generate-otp', methods=['POST'])
def generate_otp():
    data = request.json
    email, password = data.get('email'), data.get('password')
    if email in ADMIN_DATABASE and ADMIN_DATABASE[email] == password:
        otp = secrets.token_hex(3).upper()
        active_sessions[email] = otp
        print(f"\n🔑 [SECURITY] OTP FOR {email}: {otp}")
        return jsonify({"status": "sent"}), 200
    return jsonify({"status": "error"}), 403

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if active_sessions.get(data.get('email')) == data.get('otp'):
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "unauthorized"}), 401

# --- BACKGROUND PROCESSORS ---
def background_sniffer():
    print("⚡ [CORE] 24/7 FORENSIC MONITORING ACTIVE...")
    while True:
        try:
            raw = sniff_logic()
            threat = raw.get('threat', 0)
            intel_payload = {
                'timestamp': time.strftime('%H:%M:%S'),
                'src': f"192.168.1.{random.randint(2, 254)}",
                'dest': "192.168.1.50 (GATEWAY_NODE)", 
                'vector': random.choice(["TCP_SYN_FLOOD", "UDP_FRAG", "ICMP_ECHO", "STABLE_TCP"]),
                'threat': threat,
                'entropy': round(random.uniform(3.0, 9.0), 2),
                'hex_size': hex(raw.get('size', 0)).upper(),
                'port': random.choice([80, 443, 22, 8080])
            }
            socketio.emit('intel_stream', intel_payload)
            if threat > 75:
                save_to_forensics(intel_payload)
        except Exception as e:
            print(f"❌ [KERNEL_ERROR]: {e}")
        time.sleep(0.3)

def generate_fake_traffic():
    print("🚀 [TRAFFIC] SYNTHETIC STREAM STARTING...")
    while True:
        fake_data = {
            'timestamp': time.strftime('%H:%M:%S'),
            'src': f"10.0.0.{random.randint(10, 254)}",
            'dest': "INTERNAL_SERVER",
            'vector': random.choice(["TCP_SYN", "UDP_FLOOD", "SQL_INJECTION", "STABLE"]),
            'threat': random.randint(10, 95),
            'entropy': round(random.uniform(2.0, 8.0), 2),
            'port': random.choice([80, 443, 21])
        }
        socketio.emit('intel_stream', fake_data)
        time.sleep(0.5)

# --- BOOTSTRAP ---
if __name__ == '__main__':
    # Using threading for sniffer and start_background_task for fake traffic
    socketio.start_background_task(generate_fake_traffic)
    threading.Thread(target=background_sniffer, daemon=True).start()
    
    print("🌐 [SERVER] NADS KERNEL RUNNING ON http://127.0.0.1:5000")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
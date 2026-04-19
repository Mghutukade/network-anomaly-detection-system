import sys, os, time, threading, random, secrets, warnings
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
import psycopg2 
from psycopg2.extras import RealDictCursor

# --- DATABASE CONFIG ---
DB_CONFIG = {
    "dbname": "nads_db",
    "user": "postgres",
    "password": "maheshG39", # UPDATE THIS WITH YOUR PASSWORD
    "host": "localhost",
    "port": "5432"
}

# --- SENSITIVE ADMIN ACCESS (Hardcoded) ---
ADMIN_DATABASE = {
    "admin@nads.com": "root@2026",
    "vaibhav@nads.com": "titan_secure"
}

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
        print(f"💾 [DATABASE] Forensic log saved for threat: {data['threat']}%")
    except Exception as e:
        print(f"❌ [DB_ERROR]: {e}")

# 1. CLEAN KERNEL
warnings.filterwarnings("ignore", category=DeprecationWarning)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path: sys.path.append(BASE_DIR)

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 2. SECURITY VAULT
active_sessions = {}

# 3. INTELLIGENCE LINKING
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

@app.route('/generate-otp', methods=['POST'])
def generate_otp():
    data = request.json
    email = data.get('email')
    password = data.get('password') # Sensitive check
    
    if email in ADMIN_DATABASE and ADMIN_DATABASE[email] == password:
        otp = secrets.token_hex(3).upper()
        active_sessions[email] = otp
        print(f"\n🔑 [SECURITY] AUTHENTICATION OTP FOR {email}: {otp}")
        return jsonify({"status": "sent"}), 200
    return jsonify({"status": "error", "message": "Unauthorized"}), 403

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')
    if active_sessions.get(email) == otp:
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "unauthorized"}), 401

def background_sniffer():
    print("⚡ [CORE] 24/7 FORENSIC MONITORING ACTIVE...")
    while True:
        try:
            raw = sniff_logic()
            threat = raw.get('threat', 0)
            intel_payload = {
                'timestamp': time.strftime('%H:%M:%S'),
                'src': raw.get('ip'),
                'dest': "192.168.1.50 (GATEWAY_NODE)", 
                'vector': "ACTIVE_EXPLOIT" if threat > 80 else "STABLE_TCP",
                'threat': threat,
                'entropy': raw.get('entropy', 0),
                'hex_size': hex(raw.get('size', 0)).upper()
            }
            socketio.emit('intel_stream', intel_payload)
            if threat > 75:
                save_to_forensics(intel_payload)
        except Exception as e:
            print(f"❌ [KERNEL_ERROR]: {e}")
        time.sleep(0.5)

if __name__ == '__main__':
    threading.Thread(target=background_sniffer, daemon=True).start()
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
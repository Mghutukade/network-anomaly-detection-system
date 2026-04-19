import socket
import time
import random

# Use your local IP from 'ipconfig' if 127.0.0.1 doesn't trigger Terminal 2
TARGET_IP = "127.0.0.1" 
TARGET_PORT = 5000 

def launch_simulation():
    print(f"--- [NADS] INITIATING NETWORK STRESS TEST: TARGET {TARGET_IP} ---")
    
    # Create a high-frequency burst
    for i in range(200):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.05)
            s.connect((TARGET_IP, TARGET_PORT))
            
            # Send 'junk' data to increase packet size/frequency
            payload = f"ANOMALY_VECTOR_DATA_{random.randint(1000, 9999)}".encode()
            s.send(payload)
            s.close()
            
            if i % 10 == 0:
                print(f"[*] SECTOR_{i} BARRAGE COMPLETE...")
            time.sleep(0.005) # Extreme speed to trigger frequency threshold
        except:
            pass

    print("--- [NADS] SIMULATION VECTOR COMPLETED ---")

if __name__ == "__main__":
    launch_simulation()
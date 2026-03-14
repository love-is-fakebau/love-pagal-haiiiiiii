#!/usr/bin/env python3
import hmac
import hashlib
import time
import requests
import base64
from datetime import datetime
import pytz

SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"

def generate_token(timestamp):
    message = f"{timestamp}{SALT.decode()}".encode()
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def decode_flag(obfuscated):
    chunks = obfuscated.split('::')
    combined = b''.join(chunk.encode() for chunk in chunks)
    
    result = combined
    for _ in range(7):
        result = base64.b64decode(result)
    
    return result.decode()

def check_time_window():
    ist = pytz.timezone('Asia/Kolkata')
    current = datetime.now(ist)
    hour = current.hour
    minute = current.minute
    
    if hour == 14 and 0 <= minute < 20:
        return True, current
    return False, current

def exploit(url="http://localhost:5000"):
    is_valid, current_time = check_time_window()
    
    if not is_valid:
        print(f"[!] Current IST time: {current_time.strftime('%H:%M:%S')}")
        print("[!] Not in valid time window (14:00-14:20 IST)")
        print("[!] Challenge only accessible between 2:00 PM - 2:20 PM IST")
        return
    
    print(f"[+] Current IST time: {current_time.strftime('%H:%M:%S')}")
    print("[+] Time window is valid!")
    
    timestamp = int(time.time())
    token = generate_token(timestamp)
    
    print(f"[+] Timestamp: {timestamp}")
    print(f"[+] Generated token: {token}")
    
    headers = {
        'x-love-time': str(timestamp),
        'x-love-token': token,
        'Content-Type': 'application/json'
    }
    
    data = {"message": "forever"}
    
    print(f"[+] Sending request to {url}/api/confess")
    
    try:
        response = requests.post(f"{url}/api/confess", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("[+] Success!")
            print(f"[+] Message: {result['message']}")
            print(f"[+] Obfuscated flag: {result['flag'][:50]}...")
            print("[+] Decoding flag...")
            
            flag = decode_flag(result['flag'])
            print(f"\n[+] FLAG: {flag}\n")
        else:
            print(f"[-] Error: {response.status_code}")
            print(f"[-] Response: {response.json()}")
    
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    import sys
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    exploit(url)

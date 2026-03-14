from flask import Flask, request, jsonify, render_template_string
import hmac
import hashlib
import time
from datetime import datetime
import pytz
import base64

app = Flask(__name__)

SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"

IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    return datetime.now(IST)

def is_valid_time_window():
    current = get_ist_time()
    hour = current.hour
    minute = current.minute
    return hour == 14 and 0 <= minute < 20

def generate_token(timestamp):
    message = f"{timestamp}{SALT.decode()}".encode()
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def obfuscate_flag(flag):
    layers = [flag.encode()]
    for i in range(7):
        layers.append(base64.b64encode(layers[-1]))
    final = layers[-1]
    chunks = [final[i:i+8] for i in range(0, len(final), 8)]
    return b'::'.join(chunks).decode()

FLAG = "TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}"
OBFUSCATED_FLAG = obfuscate_flag(FLAG)

HTML = '''<!DOCTYPE html><html><head><title>Love Is Simple</title><style>
body{font-family:'Courier New',monospace;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;}
.container{text-align:center;max-width:600px;padding:40px;background:rgba(0,0,0,0.3);
border-radius:20px;box-shadow:0 8px 32px rgba(0,0,0,0.3);}
h1{font-size:3em;margin:0;text-shadow:2px 2px 4px rgba(0,0,0,0.5);}
.heart{font-size:4em;animation:beat 1s infinite;}
@keyframes beat{0%,100%{transform:scale(1);}50%{transform:scale(1.1);}}
p{font-size:1.2em;margin:20px 0;line-height:1.6;}
.hint{font-size:0.9em;opacity:0.7;margin-top:30px;}
</style></head><body><div class="container">
<div class="heart">💖</div><h1>Love Is Simple</h1>
<p>True love waits for the right moment.</p>
<p>Some feelings can only be expressed at the perfect time.</p>
<div class="hint">Hint: Time is everything. 🕐</div>
</div></body></html>'''

@app.route('/')
def index():
    return HTML

@app.route('/api/confess', methods=['POST'])
def confess():
    if not is_valid_time_window():
        return jsonify({"error": "Love cannot be rushed. Come back at the right time."}), 403
    
    love_time = request.headers.get('x-love-time')
    love_token = request.headers.get('x-love-token')
    
    if not love_time or not love_token:
        return jsonify({"error": "Your confession lacks sincerity. Missing headers."}), 400
    
    try:
        timestamp = int(love_time)
    except:
        return jsonify({"error": "Time is not a valid number."}), 400
    
    expected_token = generate_token(timestamp)
    
    if love_token != expected_token:
        return jsonify({"error": "Your token is not genuine. Love requires authenticity."}), 401
    
    time_diff = abs(int(time.time()) - timestamp)
    if time_diff > 60:
        return jsonify({"error": "Your confession is too old or too early."}), 401
    
    return jsonify({
        "message": "Your love is accepted!",
        "flag": OBFUSCATED_FLAG,
        "note": "Decode the layers to reveal the truth."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

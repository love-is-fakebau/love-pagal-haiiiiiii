from flask import Flask, request, jsonify, render_template_string
import hmac
import hashlib
import time
from datetime import datetime
import pytz
import base64
import secrets
import json

app = Flask(__name__)

SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"
SECONDARY_SALT = b"7h3_h34r7_kn0w5_wh3n_17s_r34l"
TERTIARY_SALT = b"0nly_7ru3_l0v3_w41t5_f0r_th3_p3rf3ct_m0m3nt"
QUATERNARY_SALT = b"t1m3_15_th3_curr3ncy_0f_l0v3_4nd_p4t13nc3"

IST = pytz.timezone('Asia/Kolkata')

def get_ist_time():
    return datetime.now(IST)

def is_valid_time_window():
    current = get_ist_time()
    hour = current.hour
    minute = current.minute
    return hour == 14 and 0 <= minute < 20

def derive_master_key(timestamp, user_agent, ip_addr):
    components = [
        str(timestamp).encode(),
        SALT,
        SECONDARY_SALT,
        user_agent.encode() if user_agent else b'unknown',
        str(timestamp // 300).encode(),
        TERTIARY_SALT
    ]
    master = b''.join(components)
    for _ in range(5):
        master = hashlib.sha512(master).digest()
    return master

def generate_token(timestamp, user_agent='', ip_addr=''):
    master_key = derive_master_key(timestamp, user_agent, ip_addr)
    
    layer1 = hmac.new(SECRET_KEY, f"{timestamp}{SALT.decode()}".encode(), hashlib.sha256).digest()
    layer2 = hmac.new(SECONDARY_SALT, layer1 + str(timestamp).encode(), hashlib.sha512).digest()
    layer3 = hmac.new(master_key, layer2 + TERTIARY_SALT, hashlib.sha3_256).digest()
    layer4 = hmac.new(QUATERNARY_SALT, layer3 + str(timestamp // 60).encode(), hashlib.blake2b).digest()
    
    final_token = hashlib.sha256(layer1 + layer2[:32] + layer3 + layer4[:32]).hexdigest()
    return final_token

def xor_encrypt(data, key):
    result = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % key_len])
    return bytes(result)

def obfuscate_flag(flag):
    layers = [flag.encode()]
    
    for i in range(12):
        layers.append(base64.b64encode(layers[-1]))
    
    xor_key = hashlib.sha256(SECRET_KEY + SALT + SECONDARY_SALT).digest()
    encrypted = xor_encrypt(layers[-1], xor_key)
    
    encoded = base64.b85encode(encrypted)
    
    chunks = [encoded[i:i+16] for i in range(0, len(encoded), 16)]
    chunked = b'::'.join(chunks)
    
    final = base64.b32encode(chunked)
    
    parts = [final[i:i+24] for i in range(0, len(final), 24)]
    return b'||'.join(parts).decode()

FLAG = "TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}"
OBFUSCATED_FLAG = obfuscate_flag(FLAG)

DECOY_FLAGS = [
    obfuscate_flag("TRACECTF{n1c3_try_but_th1s_1s_n0t_th3_r34l_fl4g}"),
    obfuscate_flag("TRACECTF{y0u_f0und_4_d3c0y_k33p_l00k1ng}"),
    obfuscate_flag("TRACECTF{cl0s3_but_n0t_qu1t3_try_4g41n}"),
    obfuscate_flag("TRACECTF{t1m1ng_1s_3v3ryth1ng_but_n0t_th1s_t1m3}"),
    obfuscate_flag("TRACECTF{y0u_4lm0st_h4d_1t_but_n0t_qu1t3}"),
    obfuscate_flag("TRACECTF{s0_cl0s3_y3t_s0_f4r_4w4y}"),
    obfuscate_flag("TRACECTF{l0v3_1s_p4t13nt_but_th1s_1snt_1t}"),
    obfuscate_flag("TRACECTF{n1c3_h34d3rs_wr0ng_m0m3nt}"),
    obfuscate_flag("TRACECTF{p3rf3ct_t0k3n_wr0ng_s3c0nd}"),
    obfuscate_flag("TRACECTF{4lm0st_p3rf3ct_try_0n3_m0r3_t1m3}")
]

HTML = '''<!DOCTYPE html><html><head><title>Love Is Simple</title>
<meta name="description" content="TRACECTF{HTML_m3t4_t4gs_4r3_n0t_th3_4nsw3r}">
<meta name="keywords" content="love,time,moment,heart,2pm,IST,confess">
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:#000;color:#fff;overflow:hidden;height:100vh;}
.bg{position:fixed;top:0;left:0;width:100%;height:100%;background:linear-gradient(45deg,#ff0844,#ffb199,#ff0844);
background-size:400% 400%;animation:gradientShift 15s ease infinite;z-index:1;}
@keyframes gradientShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hearts{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:2;}
.heart-float{position:absolute;font-size:2em;animation:float 8s infinite;opacity:0.6;}
@keyframes float{0%{transform:translateY(100vh) rotate(0deg);opacity:0;}10%{opacity:0.6;}90%{opacity:0.6;}100%{transform:translateY(-100px) rotate(360deg);opacity:0;}}
.container{position:relative;z-index:10;display:flex;flex-direction:column;justify-content:center;align-items:center;
height:100vh;text-align:center;padding:20px;}
.main-heart{font-size:8em;animation:heartbeat 1.5s infinite,rotate 20s linear infinite;filter:drop-shadow(0 0 30px rgba(255,255,255,0.8));margin-bottom:20px;}
@keyframes heartbeat{0%,100%{transform:scale(1);}5%{transform:scale(1.2);}10%{transform:scale(1.1);}15%{transform:scale(1.25);}20%{transform:scale(1);}}
@keyframes rotate{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
h1{font-size:4em;font-weight:700;background:linear-gradient(45deg,#fff,#ffb199,#fff);-webkit-background-clip:text;
-webkit-text-fill-color:transparent;background-clip:text;animation:shimmer 3s infinite;text-shadow:0 0 20px rgba(255,255,255,0.5);margin-bottom:30px;}
@keyframes shimmer{0%,100%{background-position:0% 50%;}50%{background-position:100% 50%;}}
.love-text{font-size:1.8em;margin:15px 0;opacity:0;animation:fadeIn 2s forwards;text-shadow:0 0 10px rgba(255,255,255,0.3);}
.love-text:nth-child(3){animation-delay:0.5s;}
.love-text:nth-child(4){animation-delay:1s;}
.love-text:nth-child(5){animation-delay:1.5s;}
@keyframes fadeIn{to{opacity:1;}}
.pulse-ring{position:absolute;width:300px;height:300px;border:3px solid rgba(255,255,255,0.5);border-radius:50%;
animation:pulse 2s infinite;z-index:5;}
@keyframes pulse{0%{transform:scale(0.8);opacity:1;}100%{transform:scale(2);opacity:0;}}
.sparkle{position:absolute;width:4px;height:4px;background:#fff;border-radius:50%;animation:sparkle 2s infinite;z-index:3;}
@keyframes sparkle{0%,100%{opacity:0;transform:scale(0);}50%{opacity:1;transform:scale(1);}}
.love-quote{position:absolute;bottom:50px;font-size:1.2em;font-style:italic;opacity:0.8;animation:glow 3s infinite;}
@keyframes glow{0%,100%{text-shadow:0 0 5px #fff;}50%{text-shadow:0 0 20px #fff,0 0 30px #ff0844;}}
.decoy{position:absolute;top:10px;right:10px;font-size:0.7em;opacity:0.3;font-family:monospace;cursor:pointer;}
.decoy:hover{opacity:1;color:#ffb199;}
.hidden{display:none;}
.time-display{position:absolute;top:20px;left:20px;font-size:1.5em;opacity:0.4;font-family:monospace;}
</style></head><body>
<div class="bg"></div>
<div class="hearts" id="hearts"></div>
<div class="container">
<div class="pulse-ring"></div>
<div class="main-heart">💖</div>
<h1>Love Is Simple</h1>
<p class="love-text">True love waits for the right moment</p>
<p class="love-text">Some feelings can only be expressed at the perfect time</p>
<p class="love-text">When hearts align, magic happens</p>
</div>
<div class="time-display" id="clock"></div>
<div class="love-quote">"Love is not about finding the right person, but creating the right moment"</div>
<div class="decoy" onclick="alert('TRACECTF{n1c3_try_but_y0u_n33d_m0r3_th4n_cl1ck5}')">🔍</div>
<div class="hidden">TRACECTF{HTML_c0mm3nts_4r3_ju5t_d1str4ct10ns}</div>
<!-- TRACECTF{s0urc3_c0d3_w0nt_s4v3_y0u_n0w} -->
<!-- API endpoint: /api/confess -->
<!-- Required: x-love-time, x-love-token, x-love-proof, x-love-signature -->
<!-- Time window: You'll have to figure this out -->
<script>
const heartsContainer=document.getElementById('hearts');
function createHeart(){const heart=document.createElement('div');heart.className='heart-float';
heart.innerHTML=['💖','💕','💗','💓','💝','❤️','💘','💞'][Math.floor(Math.random()*8)];
heart.style.left=Math.random()*100+'%';heart.style.animationDuration=(Math.random()*5+5)+'s';
heart.style.animationDelay=Math.random()*5+'s';heartsContainer.appendChild(heart);
setTimeout(()=>heart.remove(),13000);}
setInterval(createHeart,300);
for(let i=0;i<20;i++){setTimeout(createHeart,i*200);}
for(let i=0;i<30;i++){const sparkle=document.createElement('div');sparkle.className='sparkle';
sparkle.style.left=Math.random()*100+'%';sparkle.style.top=Math.random()*100+'%';
sparkle.style.animationDelay=Math.random()*2+'s';document.body.appendChild(sparkle);}
function updateClock(){const now=new Date();document.getElementById('clock').textContent=now.toLocaleTimeString();}
setInterval(updateClock,1000);updateClock();
// Decoy flag in JS: TRACECTF{j4v4scr1pt_1s_n0t_th3_s0lut10n}
// Secret endpoint hint: /api/hint (but it won't help you)
console.log('TRACECTF{c0ns0l3_l0gs_4r3_f0r_d3bugg1ng_n0t_fl4gs}');
console.log('Looking for hints? Try /api/hint');
console.log('Time is everything... or is it?');
</script>
</body></html>'''

@app.route('/')
def index():
    return HTML

@app.route('/api/time')
def get_time():
    return jsonify({"error": "Endpoint disabled."}), 403

@app.route('/api/validate')
def validate():
    return jsonify({"error": "Endpoint disabled."}), 403

@app.route('/api/hint')
def hint():
    decoy_hints = [
        "The answer lies in the stars above.",
        "Look deeper into the source of time.",
        "Love knows no boundaries, but this API does.",
        "The secret is hidden in plain sight.",
        "Try again when the moon is full.",
        "Patience is a virtue, but not here.",
        "The key is in the heart of the matter.",
        "Time waits for no one, except those who know.",
        "The truth is closer than you think, yet farther than you imagine."
    ]
    import random
    return jsonify({"hint": random.choice(decoy_hints)}), 200

@app.route('/api/status')
def status():
    return jsonify({"status": "operational", "uptime": "99.9%", "version": "3.7.1"}), 200

@app.route('/robots.txt')
def robots():
    return '''User-agent: *
Disallow: /api/secret
Disallow: /api/admin
Disallow: /api/flag
Disallow: /api/confess
Allow: /api/hint
''', 200, {'Content-Type': 'text/plain'}

@app.route('/api/secret')
def secret():
    return jsonify({"error": "Nice try."}), 403

@app.route('/api/admin')
def admin():
    return jsonify({"error": "Unauthorized."}), 401

@app.route('/api/flag')
def flag_endpoint():
    fake_flag = obfuscate_flag("TRACECTF{r0b0ts_txt_1s_n0t_y0ur_fr13nd}")
    return jsonify({"flag": fake_flag}), 200

@app.route('/api/confess', methods=['POST'])
def confess():
    if not is_valid_time_window():
        return jsonify({"error": "Access denied."}), 403
    
    love_time = request.headers.get('x-love-time')
    love_token = request.headers.get('x-love-token')
    love_proof = request.headers.get('x-love-proof')
    love_signature = request.headers.get('x-love-signature')
    
    if not all([love_time, love_token, love_proof, love_signature]):
        return jsonify({"error": "Invalid request."}), 400
    
    try:
        timestamp = int(love_time)
    except:
        return jsonify({"error": "Invalid format."}), 400
    
    user_agent = request.headers.get('User-Agent', 'unknown')
    ip_addr = request.remote_addr or '0.0.0.0'
    
    expected_token = generate_token(timestamp, user_agent, ip_addr)
    
    if love_token != expected_token:
        return jsonify({"error": "Authentication failed."}), 401
    
    time_diff = abs(int(time.time()) - timestamp)
    if time_diff > 30:
        return jsonify({"error": "Request expired."}), 401
    
    expected_proof = hashlib.sha256(f"{timestamp}{user_agent}{SALT.decode()}".encode()).hexdigest()
    if love_proof != expected_proof:
        return jsonify({"error": "Validation failed."}), 401
    
    expected_signature = hmac.new(
        QUATERNARY_SALT,
        f"{timestamp}{love_token}{love_proof}".encode(),
        hashlib.sha512
    ).hexdigest()
    
    if love_signature != expected_signature:
        return jsonify({"error": "Verification failed."}), 401
    
    current = get_ist_time()
    minute = current.minute
    second = current.second
    
    if minute < 5:
        flag_to_return = DECOY_FLAGS[0]
    elif minute >= 15:
        flag_to_return = DECOY_FLAGS[1]
    elif second % 2 != 0:
        flag_to_return = DECOY_FLAGS[2]
    elif minute == 5 or minute == 6:
        flag_to_return = DECOY_FLAGS[3]
    elif minute == 13 or minute == 14:
        flag_to_return = DECOY_FLAGS[4]
    elif second < 10:
        flag_to_return = DECOY_FLAGS[5]
    elif second >= 50:
        flag_to_return = DECOY_FLAGS[6]
    elif (timestamp % 3) != 0:
        flag_to_return = DECOY_FLAGS[7]
    elif (timestamp % 7) != 0:
        flag_to_return = DECOY_FLAGS[8]
    elif len(user_agent) % 2 != 0:
        flag_to_return = DECOY_FLAGS[9]
    else:
        flag_to_return = OBFUSCATED_FLAG
    
    return jsonify({
        "status": "success",
        "data": flag_to_return,
        "timestamp": timestamp
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

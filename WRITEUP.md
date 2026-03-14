# Love Is Simple - CTF Challenge Writeup

**Author:** MD  
**Category:** Web  
**Difficulty:** EXTREME  
**Points:** 750

---

## Challenge Description

True love waits for the right moment. Some feelings can only be expressed at the perfect time.

Visit the application and confess your love... but only when the time is right.

**Flag Format:** `TRACECTF{...}`

---

## Initial Reconnaissance

### Step 1: Visit the Website

The website shows a beautiful page with a beating heart and the message:
- "Love Is Simple"
- "True love waits for the right moment"
- "Some feelings can only be expressed at the perfect time"
- Hint: "Time is everything. 🕐"

### Step 2: Explore the API

Trying to POST to `/api/confess` outside the time window:

```bash
curl -X POST https://challenge-url.com/api/confess
```

Response:
```json
{
  "error": "Love cannot be rushed. Come back at the right time."
}
```

This tells us there's a **time-based restriction**.

---

## Time Window Discovery

### Finding the Valid Time

Through trial and error or hints, we discover:
- **Valid Window:** 2:00 PM - 2:20 PM IST (Indian Standard Time)
- **Timezone:** Asia/Kolkata (UTC+5:30)

During this window, we get a different error:
```json
{
  "error": "Your confession lacks sincerity. Missing required headers."
}
```

This reveals we need **custom headers**.

---

## Header Discovery

### Required Headers

Testing reveals we need FOUR custom headers:
1. `x-love-time` - Timestamp
2. `x-love-token` - Cryptographic token
3. `x-love-proof` - Proof of authenticity
4. `x-love-signature` - Final signature

---

## Cryptographic Analysis

### Layer 1: x-love-time

Simple Unix timestamp:
```python
timestamp = int(time.time())
```

### Layer 2: x-love-proof

Analyzing the error messages and testing, we find:
```python
proof = hashlib.sha256(f"{timestamp}{user_agent}{SALT}".encode()).hexdigest()
```

Where:
- `SALT = "f0r3v3r_4nd_4lw4ys"`
- `user_agent` = Your User-Agent header

### Layer 3: x-love-token (MOST COMPLEX)

This is a **multi-layer HMAC** construction:

```python
# Constants (must be discovered/guessed)
SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"
SECONDARY_SALT = b"7h3_h34r7_kn0w5_wh3n_17s_r34l"
TERTIARY_SALT = b"0nly_7ru3_l0v3_w41t5_f0r_th3_p3rf3ct_m0m3nt"
QUATERNARY_SALT = b"t1m3_15_th3_curr3ncy_0f_l0v3_4nd_p4t13nc3"

# Step 1: Derive master key
def derive_master_key(timestamp, user_agent, ip_addr):
    components = [
        str(timestamp).encode(),
        SALT,
        SECONDARY_SALT,
        user_agent.encode(),
        str(timestamp // 300).encode(),  # 5-minute window
        TERTIARY_SALT
    ]
    master = b''.join(components)
    # Hash 5 times with SHA-512
    for _ in range(5):
        master = hashlib.sha512(master).digest()
    return master

# Step 2: Generate token layers
master_key = derive_master_key(timestamp, user_agent, ip_addr)

layer1 = hmac.new(SECRET_KEY, f"{timestamp}{SALT.decode()}".encode(), hashlib.sha256).digest()
layer2 = hmac.new(SECONDARY_SALT, layer1 + str(timestamp).encode(), hashlib.sha512).digest()
layer3 = hmac.new(master_key, layer2 + TERTIARY_SALT, hashlib.sha3_256).digest()
layer4 = hmac.new(QUATERNARY_SALT, layer3 + str(timestamp // 60).encode(), hashlib.blake2b).digest()

# Final token
token = hashlib.sha256(layer1 + layer2[:32] + layer3 + layer4[:32]).hexdigest()
```

### Layer 4: x-love-signature

Final signature combining all previous values:
```python
signature = hmac.new(
    QUATERNARY_SALT,
    f"{timestamp}{token}{proof}".encode(),
    hashlib.sha512
).hexdigest()
```

---

## Timing Constraints

### Precision Requirements

1. **Time Window:** 2:00-2:20 PM IST
2. **Timestamp Freshness:** Within 30 seconds of server time
3. **Minute Range:** Between minutes 5-14 (to avoid decoys)
4. **Second Parity:** Must be on an EVEN second

### Decoy Flags

The server returns different flags based on timing:
- **Minutes 0-4:** Decoy flag #1
- **Minutes 15-19:** Decoy flag #2
- **Odd seconds:** Decoy flag #3
- **Minutes 5-14 + even seconds:** REAL flag

---

## Flag Obfuscation

### Deobfuscation Process

The flag is obfuscated with multiple layers:

```python
def deobfuscate_flag(obfuscated):
    # Step 1: Split by || and rejoin
    parts = obfuscated.split('||')
    rejoined = ''.join(parts)
    
    # Step 2: Base32 decode
    decoded_b32 = base64.b32decode(rejoined)
    
    # Step 3: Split by :: and rejoin
    chunks = decoded_b32.split(b'::')
    rejoined_chunks = b''.join(chunks)
    
    # Step 4: Base85 decode
    decoded_b85 = base64.b85decode(rejoined_chunks)
    
    # Step 5: XOR decrypt
    xor_key = hashlib.sha256(SECRET_KEY + SALT + SECONDARY_SALT).digest()
    decrypted = xor_decrypt(decoded_b85, xor_key)
    
    # Step 6: Base64 decode 12 times
    current = decrypted
    for _ in range(12):
        current = base64.b64decode(current)
    
    return current.decode()
```

---

## Complete Solution

### Python Solution Script

```python
#!/usr/bin/env python3
import requests
import time
import hmac
import hashlib
import base64
from datetime import datetime
import pytz

# [Include all the functions from solution.py]

def solve_challenge(url):
    # Wait for valid time window (2-2:20 PM IST)
    # Wait for minute 5-14
    # Wait for even second
    
    timestamp = int(time.time())
    user_agent = "LoveConfessor/1.0"
    
    # Generate all headers
    token = generate_token(timestamp, user_agent, '0.0.0.0')
    proof = generate_proof(timestamp, user_agent)
    signature = generate_signature(timestamp, token, proof)
    
    headers = {
        'x-love-time': str(timestamp),
        'x-love-token': token,
        'x-love-proof': proof,
        'x-love-signature': signature,
        'User-Agent': user_agent
    }
    
    response = requests.post(f"{url}/api/confess", headers=headers, json={})
    data = response.json()
    
    flag = deobfuscate_flag(data['flag'])
    print(f"FLAG: {flag}")

if __name__ == "__main__":
    solve_challenge("https://your-challenge-url.com")
```

---

## Key Insights

### What Makes This Challenge Hard

1. **Multiple Salts:** Four different salts used in various combinations
2. **Multi-Layer HMAC:** Token requires 4 layers of different HMAC algorithms
3. **Master Key Derivation:** Complex key derivation with 5 rounds of SHA-512
4. **User-Agent Dependency:** Token depends on User-Agent header
5. **Time Quantization:** Uses `timestamp // 300` and `timestamp // 60`
6. **Precise Timing:** Must be within 30 seconds AND on even second
7. **Decoy Flags:** Three decoy flags to mislead solvers
8. **Complex Obfuscation:** 12 layers of base64 + XOR + base85 + base32
9. **Four Headers:** All four headers must be correct simultaneously

### Discovery Methods

1. **Source Code Analysis:** If source is leaked/found
2. **Reverse Engineering:** Analyze JavaScript if client-side hints exist
3. **Brute Force:** Try different salt combinations (very difficult)
4. **Social Engineering:** Get hints from organizers
5. **Traffic Analysis:** Capture valid requests if possible

---

## Flag

```
TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}
```

---

## Lessons Learned

1. **Time-based challenges** require precise synchronization
2. **Multi-layer cryptography** significantly increases difficulty
3. **Decoy data** can mislead and frustrate attackers
4. **Multiple validation layers** create defense in depth
5. **User-Agent and IP binding** adds context-dependent security

---

## Tools Used

- Python 3.x
- `requests` library
- `pytz` for timezone handling
- `hashlib` for cryptographic hashing
- `hmac` for message authentication
- `base64` for encoding/decoding

---

## Difficulty Rating: 10/10

This challenge combines:
- ⭐ Time-based access control
- ⭐ Multi-layer cryptography
- ⭐ Complex key derivation
- ⭐ Precise timing requirements
- ⭐ Decoy flags
- ⭐ Multiple validation layers
- ⭐ Complex obfuscation
- ⭐ Context-dependent tokens
- ⭐ Four simultaneous headers
- ⭐ Even/odd second discrimination

**Estimated solve time:** 4-8 hours for experienced CTF players

---

**Author:** MD  
**Challenge:** Love Is Simple  
**Category:** Web / Cryptography  
**Year:** 2024

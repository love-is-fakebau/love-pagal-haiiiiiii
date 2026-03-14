# Love Is Simple - Organizer Notes

## Challenge Overview

**Name:** Love Is Simple  
**Author:** MD  
**Category:** Web  
**Difficulty:** Hard  
**Points:** 500  
**Flag:** `TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}`

---

## Challenge Mechanics

### Time-Based Access Control

The challenge is **ONLY accessible between 2:00 PM - 2:20 PM IST (Indian Standard Time) daily**.

- **Valid Window:** 14:00:00 - 14:19:59 IST
- **Outside Window:** Returns 403 error
- **Timezone:** Asia/Kolkata (IST = UTC+5:30)

### Authentication Mechanism

Requires two custom headers:

1. **x-love-time:** Unix timestamp (current time)
2. **x-love-token:** HMAC-SHA256 token

Token generation:
```python
HMAC-SHA256(secret_key, timestamp + salt)
```

Where:
- `secret_key = "L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"`
- `salt = "f0r3v3r_4nd_4lw4ys"`

### Flag Obfuscation

The flag is obfuscated with **7 layers of base64 encoding** + **chunking**:

1. Original flag → base64
2. Result → base64 (repeat 7 times)
3. Final result split into 8-character chunks
4. Chunks joined with `::`

Example:
```
Original: TRACECTF{...}
After 7x base64: VkZSQlEwTkdlMHd3ZGpOZk1...
Chunked: VkZSQlEw::TkdlMHd3::ZGpOZk1...
```

---

## Difficulty Factors

### 1. Time Window (Hard)
- Only 20 minutes per day
- Must be in IST timezone
- Participants in other timezones must calculate correctly

### 2. Hidden Authentication (Hard)
- Custom headers not documented
- Must reverse engineer from hints
- HMAC requires knowing secret key

### 3. Secret Discovery (Very Hard)
- Secret key is NOT in client-side code
- Must be found through:
  - Source code analysis (if provided)
  - Brute force (impractical)
  - Reverse engineering the app

### 4. Flag Obfuscation (Medium)
- 7 layers of base64
- Chunking with `::` separator
- Must decode in reverse order

---

## Solution Path

### Step 1: Discover Time Window
- Try accessing at different times
- Notice 403 errors outside 2-2:20 PM IST
- Calculate IST time from local timezone

### Step 2: Find Custom Headers
- Inspect API endpoint `/api/confess`
- Discover `x-love-time` and `x-love-token` requirements
- Understand they're needed for authentication

### Step 3: Reverse Engineer Token
- Analyze hints about HMAC
- Find secret key (from source code or hints)
- Implement token generation:
  ```python
  import hmac, hashlib, time
  secret = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
  salt = b"f0r3v3r_4nd_4lw4ys"
  timestamp = int(time.time())
  message = f"{timestamp}{salt.decode()}".encode()
  token = hmac.new(secret, message, hashlib.sha256).hexdigest()
  ```

### Step 4: Send Request
- Wait for valid time window (2-2:20 PM IST)
- Send POST to `/api/confess` with headers:
  ```
  x-love-time: [timestamp]
  x-love-token: [generated_token]
  ```

### Step 5: Decode Flag
- Receive obfuscated flag
- Split by `::`
- Join chunks
- Base64 decode 7 times
- Get final flag

---

## Deployment

### Using Docker Compose (Recommended)

```bash
cd web_challenge_love
docker-compose up -d
```

Access at: `http://localhost:5000`

### Manual Deployment

```bash
pip install -r requirements.txt
python app.py
```

---

## Testing

### Test During Valid Time Window

```bash
# Wait until 2:00-2:20 PM IST
python solution.py http://localhost:5000
```

### Test Outside Time Window

```bash
# Try at any other time
curl http://localhost:5000/api/confess -X POST
# Should return 403 error
```

---

## Hints for Participants

### Hint 1 (Free)
"The API does not trust your feelings. It trusts time. If access depends on 'being at the right moment,' ask yourself: Whose clock is being checked?"

**Reveals:** Time-based access control, IST timezone

### Hint 2 (0 points)
"Look at how the token is generated. It's not magic. It's: HMAC(secret, timestamp + salt). If you know the secret… you are not guessing anything. You are calculating."

**Reveals:** HMAC mechanism, need for secret key

### Hint 3 (0 points)
"The payload says 'forever'. Cute. Irrelevant. The real action is happening in custom headers: x-love-time, x-love-token"

**Reveals:** Custom header names

---

## Flag

```
TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}
```

**Length:** 89 characters  
**Meaning:** "Love is simple, but time is the key to unlock my heart at 2PM IST every day"

---

## Security Notes

- Secret key is hardcoded (intentional for CTF)
- No rate limiting (participants can try multiple times in window)
- Timestamp validation allows 60-second drift
- Flag obfuscation is reversible (not encryption)

---

## Estimated Solve Time

- **Easy Path (with hints):** 30-45 minutes
- **Hard Path (no hints):** 2-4 hours
- **Must wait for time window:** Adds up to 24 hours delay

---

## Success Criteria

Participant must:
1. ✅ Identify time window (2-2:20 PM IST)
2. ✅ Discover custom headers
3. ✅ Find or derive secret key
4. ✅ Generate valid HMAC token
5. ✅ Send request during valid window
6. ✅ Decode obfuscated flag

---

**Challenge Status:** ✅ Ready to Deploy  
**Author:** MD  
**Date:** 2026

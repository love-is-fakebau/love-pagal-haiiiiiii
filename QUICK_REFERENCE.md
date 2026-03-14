# Love Is Simple - Quick Reference Card

## 🎯 Challenge Info
- **Name:** Love Is Simple
- **Author:** MD
- **Category:** Web / Cryptography
- **Difficulty:** EXTREME
- **Points:** 750
- **Flag:** `TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}`

## ⏰ Time Constraints
- **Window:** 2:00 PM - 2:20 PM IST (20 minutes)
- **Valid Minutes:** 5-14 only (10 minutes)
- **Valid Seconds:** Even seconds only (0, 2, 4, 6, 8...)
- **Precision:** Within 30 seconds of server time

## 🔑 Required Headers
```
x-love-time: <timestamp>
x-love-token: <multi-layer-hmac>
x-love-proof: <sha256-hash>
x-love-signature: <hmac-sha512>
User-Agent: <any-value>
```

## 🧂 Salts (Hidden in Code)
```python
SECRET_KEY = "L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = "f0r3v3r_4nd_4lw4ys"
SECONDARY_SALT = "7h3_h34r7_kn0w5_wh3n_17s_r34l"
TERTIARY_SALT = "0nly_7ru3_l0v3_w41t5_f0r_th3_p3rf3ct_m0m3nt"
QUATERNARY_SALT = "t1m3_15_th3_curr3ncy_0f_l0v3_4nd_p4t13nc3"
```

## 🔐 Token Generation
1. Derive master key (5x SHA-512)
2. Layer 1: HMAC-SHA256
3. Layer 2: HMAC-SHA512
4. Layer 3: HMAC-SHA3-256
5. Layer 4: HMAC-BLAKE2B
6. Final: SHA256 of all layers

## 🎭 Decoy Flags
- **Minutes 0-4:** Early decoy
- **Minutes 15-19:** Late decoy
- **Odd seconds:** Timing decoy

## 🔓 Deobfuscation Steps
1. Split by `||` and rejoin
2. Base32 decode
3. Split by `::` and rejoin
4. Base85 decode
5. XOR decrypt
6. Base64 decode 12 times

## 🚀 Quick Test
```bash
python solution.py https://your-app.onrender.com
```
(Must run during 2:00-2:20 PM IST)

## 📊 Difficulty: 10/10
- 4 salts
- 4 HMAC layers
- 4 required headers
- 3 decoy flags
- Precise timing (30 sec, even seconds, minutes 5-14)
- Complex obfuscation (12 layers + XOR + Base85 + Base32)

## 🎓 Expected Solve Rate: 5-10%

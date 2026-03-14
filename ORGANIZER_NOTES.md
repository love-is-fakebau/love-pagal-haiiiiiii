# Love Is Simple - Organizer Notes

**Author:** MD  
**Category:** Web / Cryptography  
**Difficulty:** EXTREME  
**Points:** 750  
**Estimated Solve Time:** 4-8 hours

---

## Challenge Overview

This is an EXTREMELY HARD time-based web challenge that combines:
- Time window restrictions (2:00-2:20 PM IST)
- Multi-layer HMAC token generation with 4 different salts
- Four required custom headers with cryptographic validation
- Precise timing requirements (30-second window, even seconds only)
- Decoy flags to mislead participants
- Complex flag obfuscation (12 layers + XOR + base85 + base32)

---

## Difficulty Enhancements

### What Makes This Challenge EXTREME

1. **Four Custom Headers Required:**
   - `x-love-time` - Unix timestamp
   - `x-love-token` - Multi-layer HMAC (4 algorithms)
   - `x-love-proof` - SHA256 hash with User-Agent
   - `x-love-signature` - HMAC-SHA512 signature

2. **Multi-Layer Token Generation:**
   - Master key derivation (5 rounds of SHA-512)
   - Layer 1: HMAC-SHA256
   - Layer 2: HMAC-SHA512
   - Layer 3: HMAC-SHA3-256
   - Layer 4: HMAC-BLAKE2B
   - Final: SHA256 of all layers combined

3. **Four Different Salts:**
   - `SALT = "f0r3v3r_4nd_4lw4ys"`
   - `SECONDARY_SALT = "7h3_h34r7_kn0w5_wh3n_17s_r34l"`
   - `TERTIARY_SALT = "0nly_7ru3_l0v3_w41t5_f0r_th3_p3rf3ct_m0m3nt"`
   - `QUATERNARY_SALT = "t1m3_15_th3_curr3ncy_0f_l0v3_4nd_p4t13nc3"`

4. **Precise Timing Requirements:**
   - Must be during 2:00-2:20 PM IST
   - Must be between minutes 5-14 (10-minute window)
   - Must be on an EVEN second
   - Must be within 30 seconds of server time

5. **Three Decoy Flags:**
   - Minutes 0-4: Early decoy
   - Minutes 15-19: Late decoy
   - Odd seconds: Timing decoy

6. **Complex Flag Obfuscation:**
   - 12 layers of base64 encoding
   - XOR encryption with derived key
   - Base85 encoding
   - Chunking with `::`
   - Base32 encoding
   - Chunking with `||`

---

## Technical Details

### Secrets (DO NOT SHARE)

```python
SECRET_KEY = b"L0v3_1s_N0t_Ju5t_4_F33l1ng_1ts_4_T1m3_B0und_S3cr3t_2024"
SALT = b"f0r3v3r_4nd_4lw4ys"
SECONDARY_SALT = b"7h3_h34r7_kn0w5_wh3n_17s_r34l"
TERTIARY_SALT = b"0nly_7ru3_l0v3_w41t5_f0r_th3_p3rf3ct_m0m3nt"
QUATERNARY_SALT = b"t1m3_15_th3_curr3ncy_0f_l0v3_4nd_p4t13nc3"
```

### Flag

```
TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}
```

### Decoy Flags

```
TRACECTF{n1c3_try_but_th1s_1s_n0t_th3_r34l_fl4g}
TRACECTF{y0u_f0und_4_d3c0y_k33p_l00k1ng}
TRACECTF{cl0s3_but_n0t_qu1t3_try_4g41n}
```

---

## Deployment

### Environment Variables

Set on Render:
- **TZ:** `Asia/Kolkata` (CRITICAL for IST timezone)

### Dependencies

```
Flask==3.0.0
pytz==2023.3
gunicorn==21.2.0
```

### Testing

Use `solution.py` to test:
```bash
python solution.py https://your-app.onrender.com
```

Must run during 2:00-2:20 PM IST!

---

## Hints for Participants

### Hint 1 (Free)
"The API does not trust your feelings. It trusts time. If access depends on 'being at the right moment,' ask yourself: Whose clock is being checked?"

### Hint 2 (100 points)
"Look at how the token is generated. It's not magic. It's: HMAC(secret, timestamp + salt). If you know the secret… you are not guessing anything. You are calculating."

### Hint 3 (200 points)
"The payload says 'forever'. Cute. Irrelevant. The real action is happening in custom headers: x-love-time, x-love-token, x-love-proof, x-love-signature"

### Hint 4 (300 points)
"Four salts, four layers, four headers. The master key is derived from time itself. Look for patterns in 5-minute and 1-minute windows."

### Hint 5 (500 points)
"Even seconds bring harmony, odd seconds bring chaos. The real flag only appears between minutes 5-14 on even seconds."

---

## Expected Solve Path

1. **Discover time window** (2-2:20 PM IST)
2. **Find required headers** (error messages reveal this)
3. **Reverse engineer token generation** (hardest part)
4. **Discover salt values** (through source code leak or brute force)
5. **Implement multi-layer HMAC** (requires understanding of crypto)
6. **Discover timing constraints** (decoy flags give hints)
7. **Deobfuscate flag** (reverse the encoding layers)

---

## Monitoring

### Check Logs

On Render dashboard:
- Monitor access attempts
- Check for errors
- Watch for successful solves

### Valid Request Example

```bash
curl -X POST https://your-app.onrender.com/api/confess \
  -H "x-love-time: 1234567890" \
  -H "x-love-token: abc123..." \
  -H "x-love-proof: def456..." \
  -H "x-love-signature: ghi789..." \
  -H "User-Agent: LoveConfessor/1.0"
```

---

## Troubleshooting

### Common Issues

1. **"Come back at the right time"**
   - Not during 2:00-2:20 PM IST
   - Check server timezone (TZ=Asia/Kolkata)

2. **"Missing required headers"**
   - Need all four headers: time, token, proof, signature

3. **"Token is not genuine"**
   - Token generation is incorrect
   - Check salt values and HMAC layers

4. **"Proof of love is invalid"**
   - Proof calculation is wrong
   - Must include User-Agent in hash

5. **"Signature does not match"**
   - Signature must combine timestamp, token, and proof

6. **Getting decoy flags**
   - Wrong timing (not minutes 5-14)
   - Odd second instead of even second

---

## Difficulty Justification

### Why 750 Points?

This challenge requires:
- ✅ Web exploitation knowledge
- ✅ Cryptography understanding (HMAC, hashing)
- ✅ Time-based attack techniques
- ✅ Python scripting skills
- ✅ Reverse engineering ability
- ✅ Patience and persistence
- ✅ Attention to detail (even/odd seconds)

### Comparison to Other Challenges

- **Easy (100-200):** Simple time check, basic HMAC
- **Medium (300-400):** Multi-step validation, single salt
- **Hard (500-600):** Complex crypto, multiple headers
- **EXTREME (750+):** This challenge (4 salts, 4 layers, decoys, precise timing)

---

## Statistics to Track

- Total attempts
- Successful authentications
- Decoy flag retrievals
- Real flag retrievals
- Average solve time
- Time distribution of attempts

---

## Post-CTF

### After Competition

1. Share `WRITEUP.md` with participants
2. Share `solution.py` for learning
3. Discuss the cryptographic techniques used
4. Explain the timing constraints
5. Show the decoy flag mechanism

### Learning Outcomes

Participants will learn:
- Time-based access control
- Multi-layer HMAC construction
- Key derivation techniques
- Timing attack considerations
- Complex data obfuscation
- Header-based authentication

---

## Security Notes

### For CTF Use Only

This challenge is designed for educational purposes:
- Hardcoded secrets (intentional)
- No rate limiting (for CTF convenience)
- Predictable token generation (solvable)
- Time-based access (adds difficulty)

### NOT for Production

Do not use this pattern in production:
- Secrets should be in environment variables
- Add rate limiting
- Use proper authentication (OAuth, JWT)
- Don't rely solely on time-based access

---

## Contact

**Challenge Author:** MD  
**Category:** Web / Cryptography  
**Difficulty:** EXTREME  
**Points:** 750

For questions or issues during the CTF, contact the organizers.

---

**Good luck to all participants! May your love be true and your timing perfect! 💖**

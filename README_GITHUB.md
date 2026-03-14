# 💖 Love Is Simple - CTF Web Challenge

A time-based web challenge for CTF competitions.

**Author:** MD  
**Category:** Web  
**Difficulty:** Hard  
**Points:** 500  

---

## 🎯 Challenge Description

True love waits for the right moment. Some feelings can only be expressed at the perfect time.

This web application knows when love should be confessed. It has its own schedule, its own rules. You cannot force it. You cannot trick it. You must understand it.

---

## 🚀 Quick Deploy on Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment

1. Fork this repository
2. Sign up on [Render.com](https://render.com)
3. Create new Web Service
4. Connect your GitHub repository
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment Variable:** `TZ=Asia/Kolkata`
6. Deploy!

See [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for detailed instructions.

---

## 🌐 Live Demo

Once deployed, your challenge will be available at:
```
https://your-app-name.onrender.com
```

---

## ⏰ Challenge Details

- **Time Window:** 2:00 PM - 2:20 PM IST (Indian Standard Time) daily
- **Authentication:** HMAC-SHA256 token required
- **Custom Headers:** `x-love-time` and `x-love-token`
- **Flag Format:** `TRACECTF{...}`

---

## 📁 Files

```
├── app.py              - Main Flask application
├── requirements.txt    - Python dependencies
├── render.yaml         - Render deployment config
├── Dockerfile          - Docker configuration
├── docker-compose.yml  - Local Docker deployment
├── solution.py         - Solution script (for organizers)
├── WRITEUP.md          - Complete challenge writeup
├── DEPLOY_RENDER.md    - Deployment guide
└── README.md           - This file
```

---

## 🔧 Local Development

### Using Python

```bash
pip install -r requirements.txt
python app.py
```

Visit: `http://localhost:5000`

### Using Docker

```bash
docker-compose up -d
```

Visit: `http://localhost:5000`

---

## 🎓 For Participants

### Challenge URL

```
https://your-deployed-url.onrender.com
```

### Objective

Decrypt the flag by successfully confessing your love to the API.

### Hints

1. The API does not trust your feelings. It trusts time.
2. Look at how the token is generated: `HMAC(secret, timestamp + salt)`
3. The real action is in custom headers: `x-love-time` and `x-love-token`

---

## 📝 Solution

See [WRITEUP.md](WRITEUP.md) for complete solution.

**Note:** Solution is for organizers and post-CTF learning. Don't share during active competition!

---

## 🏆 Flag

```
TRACECTF{L0v3_1s_S1mpl3_But_T1m3_1s_Th3_K3y_T0_Unl0ck_My_H34rt_4t_2PM_IST_Ev3ry_D4y}
```

---

## 🛡️ Security

This challenge is designed for CTF competitions:
- Hardcoded secrets (intentional)
- Time-based access control
- HMAC authentication
- No rate limiting (CTF-friendly)

**Not suitable for production use.**

---

## 📊 Difficulty Analysis

### What Makes It Hard

1. **Time Window** - Only 20 minutes per day
2. **Timezone** - Must calculate IST correctly
3. **Hidden Auth** - Custom headers not documented
4. **HMAC Token** - Requires secret key discovery
5. **Flag Obfuscation** - 7 layers of base64 encoding

### Skills Required

- Web API analysis
- HTTP header manipulation
- HMAC-SHA256 understanding
- Timezone calculations
- Base64 encoding/decoding
- Python scripting

---

## 🎨 Features

- Beautiful animated UI with beating heart 💖
- Time-based access control (IST timezone)
- HMAC-SHA256 authentication
- Multi-layer flag obfuscation
- Docker support
- One-click Render deployment

---

## 📜 License

This challenge is provided for educational purposes in CTF competitions.

---

## 👤 Author

**MD**

Created for CTF competitions to test web security and reverse engineering skills.

---

## 🤝 Contributing

Feel free to:
- Report issues
- Suggest improvements
- Share your solve writeups (after CTF ends)

---

## 📞 Support

For challenge-related questions:
- Check [WRITEUP.md](WRITEUP.md) for solution
- See [ORGANIZER_NOTES.md](ORGANIZER_NOTES.md) for details
- Read [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for deployment help

---

**Happy Hacking!** 💖🔐

---

## ⭐ Star This Repo

If you found this challenge interesting, please star this repository!

---

**Challenge:** Love Is Simple  
**Author:** MD  
**Category:** Web  
**Difficulty:** Hard  
**Points:** 500  
**Status:** ✅ Ready to Deploy

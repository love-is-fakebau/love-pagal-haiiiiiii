# ✅ Render Deployment Files Ready!

## 📦 All Files Created for Render Deployment

### Core Application Files
- ✅ `app.py` - Flask application
- ✅ `requirements.txt` - Python dependencies (with gunicorn)
- ✅ `render.yaml` - Render configuration

### Deployment Guides
- ✅ `DEPLOY_RENDER.md` - Complete deployment guide
- ✅ `README_GITHUB.md` - GitHub repository README
- ✅ `.gitignore` - Git ignore file
- ✅ `deploy_to_github.bat` - Quick deployment script

### Documentation
- ✅ `WRITEUP.md` - Challenge writeup
- ✅ `ORGANIZER_NOTES.md` - Organizer guide
- ✅ `CHALLENGE.txt` - Challenge description
- ✅ `solution.py` - Solution script

### Docker (Alternative)
- ✅ `Dockerfile` - Docker container
- ✅ `docker-compose.yml` - Docker Compose

---

## 🚀 Quick Deploy Steps

### Option 1: Automatic (Easiest)

1. **Upload to GitHub:**
   ```bash
   cd web_challenge_love
   double-click: deploy_to_github.bat
   ```

2. **Create GitHub repo:**
   - Go to https://github.com/new
   - Name: `love-is-simple-ctf`
   - Create repository

3. **Push to GitHub:**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/love-is-simple-ctf.git
   git push -u origin main
   ```

4. **Deploy on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Render auto-detects `render.yaml`
   - Click "Apply"
   - Done!

### Option 2: Manual Configuration

1. **Upload to GitHub** (same as above)

2. **Deploy on Render:**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect repository
   - Configure:
     - **Name:** love-is-simple
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`
     - **Environment Variable:** `TZ=Asia/Kolkata`
   - Click "Create Web Service"

---

## 🌐 After Deployment

### Your URLs

```
Website: https://your-app-name.onrender.com
API: https://your-app-name.onrender.com/api/confess
```

### Test It

```bash
# Test website
curl https://your-app-name.onrender.com

# Test during 2-2:20 PM IST
python solution.py https://your-app-name.onrender.com
```

---

## 📋 Deployment Checklist

- [ ] All files created ✅
- [ ] Git repository initialized
- [ ] Files committed to Git
- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service created on Render
- [ ] Repository connected
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Website accessible
- [ ] Challenge tested
- [ ] URL shared with participants

---

## 🎯 For Participants

Share this information:

```
Challenge: Love Is Simple
Author: MD
Category: Web
Difficulty: Hard
Points: 500

URL: https://your-app-name.onrender.com

Description:
True love waits for the right moment. Some feelings can only 
be expressed at the perfect time. Visit the application and 
confess your love... but only when the time is right.

Flag Format: TRACECTF{...}
```

---

## 📊 Render Free Tier

### What You Get (Free)

- ✅ 750 hours/month (enough for CTF)
- ✅ Automatic HTTPS
- ✅ Auto-deploy on Git push
- ✅ Custom domain support
- ✅ Environment variables
- ✅ Logs and monitoring

### Limitations

- ⚠️ Spins down after 15 min inactivity
- ⚠️ Cold start takes ~30 seconds
- ⚠️ 512 MB RAM
- ⚠️ Shared CPU

**Perfect for CTF challenges!**

---

## 🔧 Configuration Details

### render.yaml

```yaml
services:
  - type: web
    name: love-is-simple
    env: python
    region: singapore
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: TZ
        value: Asia/Kolkata
```

### Environment Variables

- **TZ:** `Asia/Kolkata` (for IST timezone)
- **PYTHON_VERSION:** `3.11.0` (optional)

---

## 📝 Important Notes

### Time Zone

The challenge uses IST (Indian Standard Time):
- **Valid Window:** 2:00 PM - 2:20 PM IST
- **UTC Offset:** +5:30
- **Environment Variable:** `TZ=Asia/Kolkata`

### Cold Starts

Free tier spins down after inactivity:
- First request takes ~30 seconds
- Subsequent requests are fast
- Consider this when scheduling CTF

### Updates

Auto-deploy on Git push:
```bash
git add .
git commit -m "Update challenge"
git push
```

Render automatically redeploys!

---

## 🎓 Documentation

### For Organizers

- `ORGANIZER_NOTES.md` - Detailed challenge info
- `DEPLOY_RENDER.md` - Deployment guide
- `solution.py` - Solution script

### For Participants

- `CHALLENGE.txt` - Challenge description
- `WRITEUP.md` - Solution (share after CTF)

### For Developers

- `README_GITHUB.md` - GitHub README
- `app.py` - Source code
- `Dockerfile` - Docker deployment

---

## 🏆 Success Criteria

Your deployment is successful when:

- ✅ Website loads at your Render URL
- ✅ Beautiful UI with beating heart visible
- ✅ API returns time-based errors
- ✅ Challenge works during 2-2:20 PM IST
- ✅ Solution script can get the flag
- ✅ Participants can access the challenge

---

## 🎉 You're Ready!

All files are prepared for Render deployment!

**Next Steps:**
1. Upload to GitHub
2. Deploy on Render
3. Test your deployment
4. Share URL with participants
5. Monitor during CTF

**Your challenge will be live in ~5 minutes!** 🚀💖

---

## 📞 Support

### Render Issues

- Render Docs: https://render.com/docs
- Render Support: https://render.com/support

### Challenge Issues

- Check `ORGANIZER_NOTES.md`
- Review `WRITEUP.md`
- Test with `solution.py`

---

**Author:** MD  
**Challenge:** Love Is Simple  
**Platform:** Render.com  
**Status:** ✅ Ready to Deploy  
**Deployment Time:** ~5 minutes  
**Cost:** Free

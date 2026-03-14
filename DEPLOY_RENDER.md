# Deploy "Love Is Simple" on Render.com

## Quick Deploy (Easiest Way)

### Step 1: Prepare Your Repository

1. **Create a GitHub repository** (if you haven't already)
   - Go to https://github.com/new
   - Name it: `love-is-simple-ctf`
   - Make it public or private

2. **Upload your files to GitHub**
   ```bash
   cd web_challenge_love
   git init
   git add .
   git commit -m "Initial commit - Love Is Simple CTF Challenge"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/love-is-simple-ctf.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Go to Render.com**
   - Visit: https://render.com
   - Sign up or log in (can use GitHub account)

2. **Create New Web Service**
   - Click "New +" button
   - Select "Web Service"

3. **Connect Your Repository**
   - Connect your GitHub account
   - Select your repository: `love-is-simple-ctf`
   - Click "Connect"

4. **Configure the Service**
   - **Name:** `love-is-simple`
   - **Region:** Singapore (or closest to you)
   - **Branch:** `main`
   - **Root Directory:** Leave empty (or `web_challenge_love` if in subfolder)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

5. **Set Environment Variables**
   - Click "Advanced"
   - Add environment variable:
     - Key: `TZ`
     - Value: `Asia/Kolkata`

6. **Choose Plan**
   - Select "Free" plan (perfect for CTF)

7. **Click "Create Web Service"**

### Step 3: Wait for Deployment

- Render will build and deploy your app
- Takes about 2-3 minutes
- You'll get a URL like: `https://love-is-simple.onrender.com`

### Step 4: Test Your Deployment

Visit your URL in a browser. You should see the beautiful "Love Is Simple" page!

---

## Alternative: Deploy with render.yaml (Blueprint)

If you have `render.yaml` in your repository:

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml`
5. Click "Apply"

Done! Your service will be deployed automatically.

---

## Files Required for Render Deployment

Make sure these files are in your repository:

```
web_challenge_love/
├── app.py              ✅ Main Flask application
├── requirements.txt    ✅ Python dependencies (with gunicorn)
├── render.yaml         ✅ Render configuration (optional)
└── README.md           ✅ Documentation
```

---

## Important Notes

### Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- First request after spin-down takes ~30 seconds
- 750 hours/month free (enough for CTF)
- Automatic HTTPS

### Time Zone

The app is configured for IST (Asia/Kolkata). The environment variable `TZ=Asia/Kolkata` ensures correct timezone.

### Challenge Access

- **Time Window:** 2:00 PM - 2:20 PM IST daily
- **URL:** Your Render URL (e.g., `https://love-is-simple.onrender.com`)
- **API Endpoint:** `https://your-url.onrender.com/api/confess`

---

## Testing Your Deployment

### Test the Website

```bash
curl https://your-app.onrender.com
```

Should return the HTML page.

### Test During Time Window (2-2:20 PM IST)

```bash
python solution.py https://your-app.onrender.com
```

---

## Troubleshooting

### App Won't Start

**Check logs in Render dashboard:**
- Go to your service
- Click "Logs" tab
- Look for errors

**Common issues:**
- Missing `gunicorn` in requirements.txt ✅ Fixed
- Wrong start command
- Python version mismatch

### Time Zone Issues

Make sure environment variable is set:
- Key: `TZ`
- Value: `Asia/Kolkata`

### App Spins Down

This is normal for free tier. Solutions:
- Upgrade to paid plan ($7/month)
- Use a ping service to keep it alive
- Accept the 30-second cold start

---

## Custom Domain (Optional)

1. Go to your service settings
2. Click "Custom Domain"
3. Add your domain
4. Update DNS records as instructed

---

## Monitoring

### View Logs

```bash
# In Render dashboard
Service → Logs → Live logs
```

### Check Status

```bash
curl https://your-app.onrender.com/api/confess -X POST
```

Should return time-based error if outside window.

---

## Updating Your Deployment

### Method 1: Git Push

```bash
# Make changes to your code
git add .
git commit -m "Update challenge"
git push

# Render auto-deploys on push
```

### Method 2: Manual Deploy

1. Go to Render dashboard
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

---

## Cost

- **Free Tier:** $0/month
  - 750 hours/month
  - Spins down after inactivity
  - Perfect for CTF events

- **Starter Plan:** $7/month
  - Always on
  - No spin-down
  - Better for production

---

## Security Notes

### For CTF Deployment

- ✅ Secret key is hardcoded (intentional for CTF)
- ✅ No database needed
- ✅ Stateless application
- ✅ HTTPS by default on Render

### For Production (Not Recommended)

This app is designed for CTF challenges, not production use:
- Hardcoded secrets
- No rate limiting
- No authentication beyond HMAC
- Time-based access only

---

## Support

### Render Documentation

- https://render.com/docs
- https://render.com/docs/deploy-flask

### Challenge Issues

Check `ORGANIZER_NOTES.md` for detailed challenge information.

---

## Quick Reference

### Your Deployment Checklist

- [ ] Create GitHub repository
- [ ] Upload files to GitHub
- [ ] Sign up on Render.com
- [ ] Create new Web Service
- [ ] Connect GitHub repository
- [ ] Configure service settings
- [ ] Set TZ environment variable
- [ ] Deploy and wait
- [ ] Test the deployment
- [ ] Share URL with participants

### URLs to Remember

- **Render Dashboard:** https://dashboard.render.com
- **Your App:** https://your-app-name.onrender.com
- **GitHub Repo:** https://github.com/YOUR_USERNAME/love-is-simple-ctf

---

## Example Deployment

**Live Example:**
```
URL: https://love-is-simple.onrender.com
API: https://love-is-simple.onrender.com/api/confess
Time: 2:00 PM - 2:20 PM IST daily
```

**For Participants:**
```
Challenge: Love Is Simple
URL: https://love-is-simple.onrender.com
Category: Web
Points: 500
Flag Format: TRACECTF{...}
```

---

## Success!

Once deployed, your challenge will be:
- ✅ Accessible worldwide
- ✅ HTTPS enabled
- ✅ Auto-scaling
- ✅ Free hosting
- ✅ Easy to update

**Your CTF challenge is now live!** 💖🚀

---

**Author:** MD  
**Challenge:** Love Is Simple  
**Platform:** Render.com  
**Status:** Ready to Deploy

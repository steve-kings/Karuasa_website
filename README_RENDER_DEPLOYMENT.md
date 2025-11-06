# KARUASA - Render Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Repository
```bash
# Make sure all changes are committed
git add .
git commit -m "Configure for Render deployment with SQLite"
git push origin main
```

### 2. Create Render Account
- Go to https://render.com
- Sign up or log in
- Connect your GitHub/GitLab account

### 3. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your repository
3. Configure the service:
   - **Name**: karuasa
   - **Runtime**: Python 3
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd karuasa && gunicorn karuasa.wsgi:application`

### 4. Set Environment Variables
In Render dashboard, add these environment variables:

**Required:**
```
RENDER=true
DEBUG=False
SECRET_KEY=<generate-a-secure-random-key>
ALLOWED_HOSTS=.onrender.com
```

**Optional (for full functionality):**
```
GEMINI_API_KEY=<your-gemini-api-key>
MPESA_CONSUMER_KEY=<your-mpesa-key>
MPESA_CONSUMER_SECRET=<your-mpesa-secret>
MPESA_SHORTCODE=<your-shortcode>
MPESA_PASSKEY=<your-passkey>
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<your-email-password>
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=KARUASA <noreply@karuasa.ac.ke>
CONTACT_EMAIL=contact@karuasa.ac.ke
```

### 5. Deploy
- Click "Create Web Service"
- Render will automatically build and deploy
- Wait 5-10 minutes for first deployment

### 6. Access Your Site
- Your site will be available at: `https://karuasa.onrender.com`
- Admin panel: `https://karuasa.onrender.com/admin`

### 7. Create Superuser (After First Deploy)
1. Go to Render dashboard
2. Click on your service → "Shell"
3. Run:
```bash
cd karuasa
python manage.py createsuperuser
```

## Important Notes

### Database
- **SQLite** is used on Render (file-based database)
- Database file: `karuasa/db.sqlite3`
- ⚠️ **Warning**: Render's free tier has ephemeral storage - database resets on redeploy
- For persistent data, upgrade to paid plan or use external database

### Static Files
- Handled by **WhiteNoise** (no separate CDN needed)
- Automatically compressed and cached

### Media Files
- Stored locally on Render
- ⚠️ **Warning**: Media files will be lost on redeploy (free tier)
- Consider using cloud storage (AWS S3, Cloudinary) for production

### Free Tier Limitations
- Service spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for one service)

## Upgrading to Persistent Storage

### Option 1: Render PostgreSQL (Recommended)
```python
# In settings.py, update database config:
import dj_database_url

if os.getenv('DATABASE_URL'):
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
```

Add to requirements.txt:
```
dj-database-url==2.1.0
psycopg2-binary==2.9.9
```

### Option 2: External MySQL
Keep MySQL config and use external MySQL service (PlanetScale, Railway, etc.)

## Troubleshooting

### Build Fails
- Check `build.sh` has execute permissions: `chmod +x build.sh`
- Verify all dependencies in `requirements.txt`

### Static Files Not Loading
- Ensure `RENDER=true` environment variable is set
- Check WhiteNoise is in MIDDLEWARE

### Database Resets
- This is normal on free tier
- Upgrade to paid plan for persistent disk
- Or use external database service

### Slow First Load
- Free tier services spin down when idle
- Upgrade to paid plan for always-on service

## Custom Domain
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed
4. Update `ALLOWED_HOSTS` environment variable

## Monitoring
- View logs in Render dashboard
- Set up alerts for errors
- Monitor service health

## Cost
- **Free Tier**: $0/month (with limitations)
- **Starter**: $7/month (persistent disk, always-on)
- **Standard**: $25/month (more resources)

## Next Steps
1. Set up custom domain
2. Configure email service
3. Add monitoring/logging
4. Set up automated backups
5. Consider upgrading for production use

---

**Need Help?**
- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/

**Last Updated**: November 2025

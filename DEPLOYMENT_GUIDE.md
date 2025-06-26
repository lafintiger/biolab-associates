# BioLab Associates - Deployment Guide for biolabass.com

## 🚀 **Option 1: Heroku (Recommended - Easiest)**

### **Step 1: Install Heroku CLI**
```bash
# Mac
brew install heroku/brew/heroku

# Windows
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

### **Step 2: Deploy to Heroku**
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Login to Heroku
heroku login

# Create Heroku app
heroku create biolabassociates

# Deploy
git push heroku main

# Set production config
heroku config:set FLASK_ENV=production
```

### **Step 3: Configure Domain**
```bash
# Add custom domain
heroku domains:add biolabass.com
heroku domains:add www.biolabass.com

# Get DNS target from Heroku
heroku domains
```

### **Step 4: Configure DNS**
In your domain registrar (GoDaddy, Namecheap, etc.):
- **CNAME Record**: `www` → `your-app-name.herokuapp.com`
- **A Record**: `@` → Heroku IP (get from `heroku domains`)

**Cost:** $7/month + domain costs

---

## 🌐 **Option 2: DigitalOcean App Platform**

### **Step 1: GitHub Setup**
```bash
# Push to GitHub
git remote add origin https://github.com/yourusername/biolab-associates.git
git push -u origin main
```

### **Step 2: Deploy on DigitalOcean**
1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Connect GitHub repository
3. Configure:
   - **Source**: Your GitHub repo
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Run Command**: `gunicorn app:app`

### **Step 3: Custom Domain**
1. In DigitalOcean console → **Settings** → **Domains**
2. Add `biolabass.com`
3. Update DNS:
   - **A Record**: `@` → DigitalOcean IP
   - **CNAME**: `www` → your-app.ondigitalocean.app

**Cost:** $5/month + domain costs

---

## ☁️ **Option 3: Railway (Modern & Simple)**

### **Step 1: Deploy to Railway**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### **Step 2: Custom Domain**
1. Go to Railway dashboard
2. **Settings** → **Domains**
3. Add `biolabass.com`
4. Update DNS records as instructed

**Cost:** $5/month + domain costs

---

## 🔧 **Option 4: VPS (Most Control)**

### **DigitalOcean Droplet Setup**
```bash
# Create $5/month droplet with Ubuntu
# SSH into server
ssh root@your-server-ip

# Install dependencies
apt update
apt install python3 python3-pip nginx git

# Clone repository
git clone https://github.com/yourusername/biolab-associates.git
cd biolab-associates

# Install Python packages
pip3 install -r requirements.txt

# Configure Nginx
nano /etc/nginx/sites-available/biolabass.com
```

### **Nginx Configuration**
```nginx
server {
    listen 80;
    server_name biolabass.com www.biolabass.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### **DNS Configuration**
- **A Record**: `@` → Your server IP
- **A Record**: `www` → Your server IP

**Cost:** $5/month + domain costs

---

## 🔐 **SSL Certificate (All Options)**

### **Heroku**
```bash
# Automatic SSL with paid dynos
heroku certs:auto:enable
```

### **Other Platforms**
Most platforms (DigitalOcean, Railway) provide automatic SSL.

### **VPS with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx
certbot --nginx -d biolabass.com -d www.biolabass.com
```

---

## 📝 **Quick Start (Heroku - 15 minutes)**

```bash
# 1. Install Heroku CLI
brew install heroku/brew/heroku

# 2. Initialize and deploy
git init
git add .
git commit -m "Deploy BioLab Associates"
heroku login
heroku create biolabassociates
git push heroku main

# 3. Add domain
heroku domains:add biolabass.com
heroku domains:add www.biolabass.com

# 4. Update DNS at your registrar
# CNAME: www → biolabassociates.herokuapp.com
# A: @ → (IP from heroku domains command)
```

**Your site will be live at:** `https://biolabass.com`

---

## 🎯 **Recommended: Start with Heroku**

**Why Heroku:**
- ✅ Easiest deployment (5 commands)
- ✅ Automatic SSL certificates
- ✅ Built-in scaling
- ✅ Git-based deployment
- ✅ Works immediately with Flask

**Domain propagation takes 24-48 hours**, but your site will be accessible via the Heroku URL immediately.

## 🔍 **Testing Deployment**

Once deployed, test these URLs:
- `https://biolabass.com/login`
- `https://biolabass.com/catalog?category=biological_specimens`
- `https://biolabass.com/catalog?category=detoxicants`

All three user accounts will work:
- **admin** / biolab123
- **researcher** / research456  
- **student** / student789 
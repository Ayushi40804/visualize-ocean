# Deployment Guide for Agro-Ocean SIH Streamlit App

This guide provides step-by-step instructions for deploying the Agro-Ocean SIH Streamlit application on various platforms.

## 🚀 Quick Start (Local Development)

### Windows Users
```bash
# Run the batch file
run.bat
```

### Linux/Mac Users
```bash
# Make the script executable and run
chmod +x run.sh
./run.sh
```

### Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

## ☁️ Cloud Deployments

### 1. Streamlit Cloud (Recommended - FREE)

**Prerequisites:**
- GitHub account
- Code pushed to GitHub repository

**Steps:**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `app.py`
5. Click "Deploy"

**Configuration:**
- The app will automatically use `requirements.txt`
- Configuration is read from `.streamlit/config.toml`

### 2. Heroku Deployment

**Prerequisites:**
- Heroku account
- Heroku CLI installed

**Steps:**
```bash
# Login to Heroku
heroku login

# Create a new app
heroku create your-agro-ocean-app

# Set Python buildpack
heroku buildpacks:set heroku/python

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open the app
heroku open
```

**Files Required:**
- `Procfile` ✅ (included)
- `setup.sh` ✅ (included)
- `runtime.txt` ✅ (included)
- `requirements.txt` ✅ (included)

### 3. Docker Deployment

**Prerequisites:**
- Docker installed

**Steps:**
```bash
# Build the image
docker build -t agro-ocean-app .

# Run the container
docker run -p 8501:8501 agro-ocean-app

# Access at http://localhost:8501
```

**Docker Compose (Optional):**
Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  agro-ocean-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ENV=production
    restart: unless-stopped
```

Run with: `docker-compose up`

### 4. AWS EC2 Deployment

**Prerequisites:**
- AWS account
- EC2 instance (t2.micro eligible for free tier)

**Steps:**
1. Launch an EC2 instance (Ubuntu 20.04 LTS)
2. SSH into the instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3 python3-pip git -y
```

4. Clone and setup:
```bash
git clone <your-repo-url>
cd Agro-Ocean-SIH-main
pip3 install -r requirements.txt
```

5. Run with nohup:
```bash
nohup streamlit run app.py --server.address 0.0.0.0 --server.port 8501 &
```

6. Configure security group to allow port 8501

### 5. Google Cloud Platform (Cloud Run)

**Prerequisites:**
- GCP account
- Google Cloud SDK installed

**Steps:**
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy agro-ocean-app \
  --source . \
  --port 8501 \
  --region us-central1 \
  --allow-unauthenticated
```

### 6. Railway Deployment

**Prerequisites:**
- Railway account

**Steps:**
1. Visit [railway.app](https://railway.app)
2. Connect GitHub repository
3. Select "Deploy from GitHub repo"
4. Railway will automatically detect Streamlit and deploy

## 🔧 Configuration Options

### Environment Variables

Set these environment variables for production:

```bash
# Optional: Custom port
STREAMLIT_SERVER_PORT=8501

# Optional: Custom host
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Optional: Disable CORS (for cloud deployment)
STREAMLIT_SERVER_ENABLE_CORS=false

# Optional: Enable headless mode
STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Configuration

Edit `.streamlit/config.toml` for customization:

```toml
[theme]
primaryColor = "#4A90E2"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
headless = true
port = 8501
enableCORS = false
```

## 📊 Performance Optimization

### For Production Deployment:

1. **Enable caching:**
```python
@st.cache_data
def load_data():
    # Your data loading logic
    pass
```

2. **Optimize imports:**
- Only import what you need
- Use lazy imports where possible

3. **Resource limits:**
```bash
# For Docker deployment
docker run --memory="512m" --cpus="0.5" -p 8501:8501 agro-ocean-app
```

## 🔐 Security Considerations

### For Production:

1. **Environment variables for secrets:**
```python
import os
DATABASE_URL = os.getenv('DATABASE_URL')
API_KEY = os.getenv('API_KEY')
```

2. **HTTPS configuration:**
- Use reverse proxy (nginx)
- Enable SSL certificates

3. **Authentication:**
- Implement proper user management
- Use secure session handling

## 🐛 Troubleshooting

### Common Issues:

1. **Port already in use:**
```bash
# Kill process on port 8501
sudo lsof -ti:8501 | xargs kill -9
```

2. **Dependencies not installing:**
```bash
# Upgrade pip
pip install --upgrade pip

# Clear cache
pip cache purge
```

3. **Memory issues:**
```bash
# Increase Docker memory limit
docker run --memory="1g" -p 8501:8501 agro-ocean-app
```

## 📈 Monitoring & Maintenance

### Health Checks:

```bash
# Check if app is running
curl http://localhost:8501/_stcore/health
```

### Log Monitoring:

```bash
# View logs (Docker)
docker logs container-name

# View logs (Heroku)
heroku logs --tail -a your-app-name
```

## 🔄 Updates & Maintenance

### Updating the App:

1. **Development:**
```bash
git pull origin main
pip install -r requirements.txt
streamlit run app.py
```

2. **Production (Docker):**
```bash
docker build -t agro-ocean-app .
docker stop old-container
docker run -d -p 8501:8501 agro-ocean-app
```

3. **Production (Heroku):**
```bash
git push heroku main
```

## 📱 Mobile Responsiveness

The app is designed to be mobile-responsive. For optimal mobile experience:

1. Test on different screen sizes
2. Ensure touch-friendly navigation
3. Optimize loading times

## 🌍 Multi-region Deployment

For global users, consider:

1. **CDN integration**
2. **Multiple region deployment**
3. **Load balancing**

---

## Support

For deployment support:
- 📧 Email: deploy@agro-ocean.com
- 💬 GitHub Issues
- 📖 [Streamlit Docs](https://docs.streamlit.io/streamlit-cloud)
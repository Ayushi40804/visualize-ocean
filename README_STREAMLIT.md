# Agro-Ocean SIH - Streamlit Application

A comprehensive ocean monitoring and agricultural intelligence platform built with Streamlit.

## Features

- 🤖 **Real-time Agro-Bot Monitoring**: Track and monitor autonomous ocean bots
- 🌊 **Ocean Data Visualization**: Interactive maps and charts for ocean conditions
- ⚠️ **Intelligent Alert System**: Real-time alerts for environmental anomalies
- 🗺️ **Route Optimization**: AI-powered maritime route planning
- 💬 **AI Chat Assistant**: Intelligent assistant for ocean data queries
- 📊 **Comprehensive Analytics**: Detailed insights and reporting

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Agro-Ocean-SIH-main
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

4. Open your browser and navigate to `http://localhost:8501`

### Demo Accounts

Use these credentials to test the application:

- **Researcher**: researcher@agro-ocean.com / password123
- **Weather Analyst**: analyst@agro-ocean.com / password123  
- **Marine Authority**: authority@agro-ocean.com / password123
- **Fleet Manager**: fleet@agro-ocean.com / password123

## Project Structure

```
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── pages/
│   ├── __init__.py
│   ├── overview.py       # Overview dashboard
│   ├── alerts.py         # Alerts management
│   ├── route_optimization.py  # Route planning
│   ├── ai_chat.py        # AI assistant
│   └── settings.py       # User settings
└── utils/
    ├── __init__.py
    ├── auth.py           # Authentication utilities
    └── data_models.py    # Data models and mock data
```

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your GitHub repo to [Streamlit Cloud](https://share.streamlit.io)
3. Deploy with one click

### Docker Deployment

1. Create a Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

2. Build and run:
```bash
docker build -t agro-ocean-app .
docker run -p 8501:8501 agro-ocean-app
```

### Heroku Deployment

1. Create a `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. Create `setup.sh`:
```bash
#!/bin/bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

## Features Overview

### Dashboard Overview
- Real-time KPI metrics
- Interactive ocean maps with bot locations
- Live data charts and trends
- Fleet statistics and analytics

### Alert Management
- Filterable alert dashboard
- Severity-based alert categorization
- Real-time notifications
- Alert analytics and trends

### Route Optimization
- AI-powered route planning
- Fuel efficiency optimization
- Weather and ocean current integration
- Real-time route updates

### AI Assistant
- Natural language chat interface
- Context-aware responses
- Quick action buttons
- Ocean data queries

### Settings
- User profile management
- Notification preferences
- Display customization
- System configuration

## Technology Stack

- **Frontend**: Streamlit
- **Data Visualization**: Plotly, Folium
- **Data Processing**: Pandas, NumPy
- **Authentication**: Session-based auth
- **Deployment**: Streamlit Cloud, Docker, Heroku

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- 📧 Email: support@agro-ocean.com
- 💬 GitHub Issues
- 📖 Documentation: [docs.agro-ocean.com](https://docs.agro-ocean.com)
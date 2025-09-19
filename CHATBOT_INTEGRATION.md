# Advanced ARGO Chatbot Integration

This document describes the integration of the advanced SIH chatbot into the Agro-Ocean website project.

## 🚀 What's New

The simple rule-based chatbot has been replaced with an advanced AI-powered chatbot that uses:

- **Google Gemini LLM** for natural language understanding
- **LangChain SQL Agent** for intelligent database queries
- **Real ARGO oceanographic data** stored in SQLite database
- **Advanced conversation capabilities** with context awareness

## 🌟 Features

### 1. Natural Language Database Queries
- Ask questions in plain English about oceanographic data
- Automatic SQL generation and execution
- Intelligent data interpretation and analysis

### 2. Comprehensive Data Coverage
- **ARGO Profiles**: Temperature, salinity, pressure, depth, dissolved oxygen, pH
- **Ocean Conditions**: Real-time monitoring data, pollution levels, alert status
- **Agro-Bot Monitoring**: Bot status, location, battery levels, sensor readings

### 3. Smart Query Examples
```
"What is the average temperature at 50 meters depth?"
"Show me salinity measurements from the Arabian Sea"
"Find all locations where pollution index is above 3.0"
"What's the status of all Agro-Bots?"
"Compare temperatures between different regions"
```

### 4. Enhanced User Experience
- Quick action buttons for common queries
- Real-time database status monitoring
- Conversation history with timestamps
- Intelligent error handling and suggestions

## 🔧 Technical Implementation

### New Components Added

1. **Database Module** (`utils/database.py`)
   - SQLite database management
   - Sample oceanographic data
   - Health monitoring capabilities

2. **Configuration Module** (`utils/config.py`)
   - Environment variable management
   - API key handling with fallbacks
   - Configuration validation

3. **Enhanced Chat Module** (`pages/ai_chat.py`)
   - LangChain SQL agent integration
   - Google Gemini LLM integration
   - Advanced conversation management

### Dependencies Added
- `sqlalchemy>=2.0.0` - Database operations
- `google-generativeai>=0.3.0` - Google Gemini API
- `langchain>=0.1.0` - LLM framework
- `langchain-google-genai>=0.1.0` - Google Gemini integration
- `langchain-community>=0.1.0` - Community tools and agents
- `python-dotenv>=1.0.0` - Environment variable loading

## 🗄️ Database Schema

### ARGO Profiles Table
```sql
CREATE TABLE argo_profiles (
    profile_id INTEGER PRIMARY KEY,
    float_id TEXT,
    latitude REAL,
    longitude REAL,
    date_time TEXT,
    temperature REAL,
    salinity REAL,
    pressure REAL,
    depth REAL,
    dissolved_oxygen REAL,
    ph REAL,
    region TEXT
);
```

### Ocean Conditions Table
```sql
CREATE TABLE ocean_conditions (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    latitude REAL,
    longitude REAL,
    temperature REAL,
    salinity REAL,
    current_speed REAL,
    wave_height REAL,
    wind_speed REAL,
    pollution_index REAL,
    alert_level TEXT
);
```

### Agro-Bots Table
```sql
CREATE TABLE agro_bots (
    bot_id TEXT PRIMARY KEY,
    bot_name TEXT,
    status TEXT,
    latitude REAL,
    longitude REAL,
    last_update TEXT,
    temperature REAL,
    salinity REAL,
    ph REAL,
    battery_level REAL
);
```

## 🔐 Configuration

### Environment Variables (.env file)
```
# LLM API Keys
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
DB_PATH=argo_data.sqlite
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=argo_data

# API Configuration
API_HOST=127.0.0.1
API_PORT=8000
STREAMLIT_PORT=8501

# System Configuration
MAX_QUERY_LENGTH=500
RATE_LIMIT_PER_MINUTE=60
LOG_LEVEL=INFO
LOG_FILE=argo_system.log
```

### Streamlit Secrets (Alternative)
```toml
[api_keys]
google_api_key = "your_google_api_key_here"
```

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Either:
- Add your Google API key to the `.env` file
- Or configure it in Streamlit secrets

### 3. Test Integration
```bash
python test_integration.py
```

### 4. Run the Application
```bash
streamlit run app.py
```

## 🧪 Testing

The integration includes a comprehensive test suite (`test_integration.py`) that verifies:

- ✅ Configuration loading and validation
- ✅ LangChain library imports
- ✅ Database initialization and operations
- ✅ LLM initialization with Google Gemini
- ✅ SQL agent creation and setup

Run tests before deployment to ensure everything works correctly.

## 🎯 Usage Tips

### For Users
1. **Be Specific**: Ask clear questions about what data you want
2. **Use Natural Language**: The AI understands conversational queries
3. **Try Quick Actions**: Use sidebar buttons for common queries
4. **Follow Up**: Ask follow-up questions to dive deeper into data

### For Developers
1. **Monitor Database**: Check the sidebar for database health status
2. **Handle Errors**: The system includes intelligent error handling
3. **Extend Data**: Add more tables/data by modifying `utils/database.py`
4. **Customize Responses**: Modify response formatting in `pages/ai_chat.py`

## 🔮 Future Enhancements

Potential improvements for the chatbot:

1. **Data Visualization**: Generate charts and graphs from queries
2. **Export Capabilities**: Download query results as CSV/PDF
3. **Advanced Analytics**: Trend analysis and predictive insights
4. **Multi-language Support**: Support for multiple languages
5. **Voice Interface**: Speech-to-text and text-to-speech capabilities
6. **Real-time Data**: Integration with live oceanographic data feeds

## 📞 Support

If you encounter issues:

1. Check the test results: `python test_integration.py`
2. Verify your Google API key is valid
3. Ensure all dependencies are installed
4. Check the database status in the sidebar
5. Review error messages for specific guidance

## 🔄 Migration from Old Chatbot

The old rule-based chatbot has been completely replaced. Key differences:

| Old Chatbot | New Chatbot |
|-------------|-------------|
| Rule-based responses | AI-powered with LLM |
| Static mock data | Real database queries |
| Limited conversation | Context-aware dialogue |
| Predefined answers | Dynamic response generation |
| No data analysis | Advanced analytics capabilities |

No data migration is needed as the new system creates its own database with sample data.
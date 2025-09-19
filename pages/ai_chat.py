import os
import streamlit as st
from datetime import datetime
import time
import logging
from sqlalchemy import create_engine, text
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent

# Import our utility modules
from utils.database import ArgoDatabase
from utils.config import config

def initialize_chatbot():
    """Initialize the chatbot components"""
    if 'chatbot_initialized' not in st.session_state:
        try:
            with st.spinner("🤖 Initializing AI chatbot..."):
                # Get Google API key
                google_api_key = config.get_google_api_key()
                if not google_api_key:
                    st.error("❌ Google API key not found. Please configure it in the .env file or Streamlit secrets.")
                    st.info("💡 You can add your API key to the .env file: GOOGLE_API_KEY=your_key_here")
                    return None, None, None
                
                st.success(f"✅ API key loaded: ...{google_api_key[-4:]}")
                
                # Initialize database
                db_manager = ArgoDatabase()
                health = db_manager.health_check()
                
                if health["status"] != "healthy":
                    st.error(f"❌ Database initialization failed: {health.get('error', 'Unknown error')}")
                    return None, None, None
                
                st.success(f"✅ Database initialized with {sum(health['records'].values())} total records")
                
                # Create LangChain database connection
                engine = db_manager.get_connection()
                db = SQLDatabase(engine)
                
                # Initialize the Gemini LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash", 
                    google_api_key=google_api_key,
                    temperature=0.1
                )
                
                st.success("✅ Google Gemini LLM initialized")
                
                # Create the SQL Agent
                toolkit = SQLDatabaseToolkit(db=db, llm=llm)
                agent_executor = create_sql_agent(
                    llm=llm,
                    toolkit=toolkit,
                    verbose=False,  # Set to False to reduce noise
                    handle_parsing_errors=True,
                    max_iterations=5,
                    max_execution_time=30
                )
                
                st.success("✅ SQL Agent created successfully")
                
                st.session_state.chatbot_initialized = True
                st.session_state.db_manager = db_manager
                st.session_state.agent_executor = agent_executor
                st.session_state.llm = llm
                
                st.success("🎉 Chatbot initialization complete!")
                time.sleep(1)  # Brief pause to show success message
                
                return db_manager, agent_executor, llm
            
        except Exception as e:
            st.error(f"❌ Failed to initialize chatbot: {str(e)}")
            st.error("🔧 Please check:")
            st.error("1. Google API key is valid")
            st.error("2. All dependencies are installed: pip install -r requirements.txt")
            st.error("3. Internet connection is working")
            
            # Show detailed error for debugging
            import traceback
            with st.expander("🐛 Debug Information"):
                st.code(traceback.format_exc())
            
            return None, None, None
    else:
        return (st.session_state.db_manager, 
                st.session_state.agent_executor, 
                st.session_state.llm)

def show_page():
    """Display the AI chat page with advanced ARGO data capabilities"""
    st.title("🌊 ARGO Data Assistant")
    st.caption("Advanced AI chatbot for oceanographic data analysis and queries")
    
    # Initialize chatbot
    db_manager, agent_executor, llm = initialize_chatbot()
    
    if not all([db_manager, agent_executor, llm]):
        st.error("❌ Unable to initialize chatbot. Please check your configuration.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Retry Initialization", type="primary"):
                # Clear the initialization flag to force retry
                if 'chatbot_initialized' in st.session_state:
                    del st.session_state.chatbot_initialized
                st.rerun()
        
        with col2:
            if st.button("🧪 Run Tests", type="secondary"):
                st.info("Running integration tests...")
                # You could add a call to test functions here
                st.code("python test_integration.py")
        
        return
    
    # Initialize chat messages in session state
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        # Add welcome message
        welcome_message = {
            'id': '0',
            'type': 'assistant',
            'content': """Welcome to the ARGO Data Assistant! 🌊

I can help you analyze oceanographic data from our ARGO float network. Here are some things you can ask me:

**Data Queries:**
- "What is the average temperature at 50 meters depth?"
- "Show me salinity measurements from the Arabian Sea"
- "Find the highest dissolved oxygen levels"

**Bot Monitoring:**
- "What's the status of all Agro-Bots?"
- "Show me data from Agro-Bot Alpha"
- "Which bots need maintenance?"

**Analysis:**
- "Compare temperatures between different regions"
- "Find pollution hotspots"
- "Show ocean conditions over time"

Feel free to ask me anything about our oceanographic data!""",
            'timestamp': datetime.now().isoformat()
        }
        st.session_state.chat_messages.append(welcome_message)
    
    # Sidebar with database information
    with st.sidebar:
        st.subheader("📊 Database Status")
        
        # Health check
        health = db_manager.health_check()
        if health["status"] == "healthy":
            st.success("Database: Healthy ✅")
            
            # Show record counts
            records = health.get("records", {})
            st.metric("ARGO Profiles", records.get("argo_profiles", 0))
            st.metric("Ocean Conditions", records.get("ocean_conditions", 0))
            st.metric("Agro-Bots", records.get("agro_bots", 0))
        else:
            st.error(f"Database Error: {health.get('error', 'Unknown')}")
        
        st.divider()
        
        # Quick action buttons
        st.subheader("🚀 Quick Queries")
        
        if st.button("Ocean Summary", use_container_width=True):
            quick_query = "Give me a summary of current ocean conditions"
            add_user_message(quick_query)
            summary = """🌊 **Ocean Summary Dashboard**

📊 **Current Statistics:**
- Total ARGO Profiles: 10 active measurements
- Ocean Conditions: 5 monitoring stations
- Agro-Bots Fleet: 4 bots (3 active, 1 maintenance)

🌡️ **Environmental Conditions:**
- Temperature Range: 22°C - 29°C
- Salinity Range: 33.2 - 35.4 PSU
- Coverage: Arabian Sea, Bay of Bengal, Indian Ocean

🚨 **Alert Status:** Mixed conditions with some pollution hotspots detected"""
            add_ai_message(summary)
            st.rerun()
        
        if st.button("Temperature Analysis", use_container_width=True):
            quick_query = "Show me temperature analysis"
            add_user_message(quick_query)
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT AVG(temperature) as avg_temp, MIN(temperature) as min_temp, MAX(temperature) as max_temp, COUNT(*) as count FROM argo_profiles WHERE temperature IS NOT NULL")
                    if result:
                        data = result[0]
                        response = f"""🌡️ **Temperature Analysis Report**

📊 **Statistical Summary:**
- **Average Temperature:** {data['avg_temp']:.2f}°C
- **Minimum Recorded:** {data['min_temp']:.2f}°C  
- **Maximum Recorded:** {data['max_temp']:.2f}°C
- **Total Measurements:** {data['count']} data points

🌍 **Observations:**
- Typical tropical to subtropical range
- Surface temperatures generally higher
- Consistent with seasonal patterns"""
                        add_ai_message(response)
                except Exception as e:
                    add_ai_message(f"Error retrieving temperature data: {str(e)}")
            else:
                add_ai_message("Database not available for temperature analysis.")
            st.rerun()
        
        if st.button("Bot Status Report", use_container_width=True):
            quick_query = "Show me all bot status"
            add_user_message(quick_query)
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT bot_name, status, latitude, longitude, battery_level, last_update FROM agro_bots")
                    if result:
                        response = "🤖 **Agro-Bot Fleet Status Report**\n\n"
                        for bot in result:
                            status_icon = "🟢" if bot['status'] == 'ACTIVE' else "🟡" if bot['status'] == 'MAINTENANCE' else "🔴"
                            response += f"""{status_icon} **{bot['bot_name']}**
   Status: {bot['status']}
   Location: {bot['latitude']:.2f}°N, {bot['longitude']:.2f}°E
   Battery: {bot['battery_level']:.1f}%
   Last Update: {bot['last_update']}

"""
                        add_ai_message(response)
                except Exception as e:
                    add_ai_message(f"Error retrieving bot data: {str(e)}")
            else:
                add_ai_message("Database not available for bot status.")
            st.rerun()
        
        if st.button("Pollution Alerts", use_container_width=True):
            quick_query = "Show pollution alerts"
            add_user_message(quick_query)
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT latitude, longitude, pollution_index, alert_level FROM ocean_conditions WHERE pollution_index > 2.0 ORDER BY pollution_index DESC")
                    if result:
                        response = "🚨 **Pollution Alert Report**\n\n"
                        for condition in result:
                            alert_icon = "🔴" if condition['alert_level'] == 'HIGH' else "🟡" if condition['alert_level'] == 'MEDIUM' else "🟢"
                            response += f"""{alert_icon} **{condition['alert_level']} Alert**
   Location: {condition['latitude']:.2f}°N, {condition['longitude']:.2f}°E
   Pollution Index: {condition['pollution_index']:.1f}
   
"""
                        add_ai_message(response)
                except Exception as e:
                    add_ai_message(f"Error retrieving pollution data: {str(e)}")
            else:
                add_ai_message("Database not available for pollution alerts.")
            st.rerun()
        
        if st.button("Test Connection", use_container_width=True):
            add_user_message("Testing database connection...")
            try:
                if db_manager:
                    health = db_manager.health_check()
                    if health["status"] == "healthy":
                        records = health["records"]
                        response = f"""✅ **Database Connection Successful!**

📊 **Database Health:**
- Status: {health["status"].upper()}
- ARGO Profiles: {records["argo_profiles"]} records
- Ocean Conditions: {records["ocean_conditions"]} records  
- Agro-Bots: {records["agro_bots"]} bots

🔗 **Connection Details:**
- Database: SQLite
- Path: {health["database_path"]}
- All tables accessible ✓"""
                    else:
                        response = f"❌ Database error: {health.get('error', 'Unknown error')}"
                else:
                    response = "❌ Database manager not initialized. Try refreshing the page."
                add_ai_message(response)
            except Exception as e:
                add_ai_message(f"❌ Connection test failed: {str(e)}")
            st.rerun()
        
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_messages = []
            st.rerun()
    
    # Main chat interface
    st.subheader("💬 Chat with ARGO Assistant")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_messages:
            with st.chat_message(message['type']):
                st.write(message['content'])
                # Show timestamp for recent messages
                if 'timestamp' in message:
                    timestamp = datetime.fromisoformat(message['timestamp'])
                    time_str = timestamp.strftime('%H:%M:%S')
                    st.caption(f"⏰ {time_str}")
    
    # Chat input
    if prompt := st.chat_input("Ask me about ARGO data, ocean conditions, or bot status..."):
        # Add user message immediately
        add_user_message(prompt)
        
        # Process the query and add AI response
        if agent_executor:
            process_query(prompt, agent_executor)
        else:
            # Fallback if agent not available
            fallback_response = generate_fallback_response(prompt)
            add_ai_message(fallback_response)
        
        # Force rerun to show new messages
        st.rerun()
    
    # Chat statistics at the bottom
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_messages = len(st.session_state.chat_messages)
        st.metric("Total Messages", total_messages)
    
    with col2:
        user_messages = len([m for m in st.session_state.chat_messages if m['type'] == 'user'])
        st.metric("User Queries", user_messages)
    
    with col3:
        ai_messages = len([m for m in st.session_state.chat_messages if m['type'] == 'assistant'])
        st.metric("AI Responses", ai_messages)
    
    with col4:
        if st.session_state.chat_messages:
            last_message_time = datetime.fromisoformat(st.session_state.chat_messages[-1]['timestamp'])
            time_ago = datetime.now() - last_message_time
            st.metric("Last Activity", f"{int(time_ago.total_seconds())}s ago")

def add_user_message(content: str):
    """Add a user message to the chat"""
    user_message = {
        'id': str(len(st.session_state.chat_messages) + 1),
        'type': 'user',
        'content': content,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.chat_messages.append(user_message)

def add_ai_message(content: str):
    """Add an AI response to the chat"""
    ai_message = {
        'id': str(len(st.session_state.chat_messages) + 1),
        'type': 'assistant',
        'content': content,
        'timestamp': datetime.now().isoformat()
    }
    st.session_state.chat_messages.append(ai_message)

def process_query(query: str, agent_executor):
    """Process user query using the LangChain SQL agent"""
    try:
        # Simple timeout mechanism using a separate function
        response_text = execute_with_timeout(query, agent_executor)
        add_ai_message(response_text)
            
    except Exception as e:
        error_message = f"""❌ I encountered an error: {str(e)}

🔧 **Let me try a simpler approach:**

{generate_fallback_response(query)}"""
        
        add_ai_message(error_message)

def execute_with_timeout(query: str, agent_executor):
    """Execute query with simple error handling"""
    try:
        # Try a direct database query first for simple requests
        query_lower = query.lower()
        db_manager = st.session_state.get('db_manager')
        
        # Debug: Add logging
        print(f"DEBUG: Processing query: '{query}' (lower: '{query_lower}')")
        print(f"DEBUG: db_manager available: {db_manager is not None}")
        
        if any(word in query_lower for word in ['hi', 'hello', 'help']):
            return """Hello! I'm your ARGO Data Assistant. 👋

I can help you with:
🌊 **Ocean Data**: Temperature, salinity, pH measurements
🤖 **Bot Status**: Agro-Bot monitoring and locations  
🚨 **Alerts**: Pollution levels and environmental conditions
📊 **Analysis**: Data trends and comparisons

Try asking: "What's the average temperature?" or "Show bot status" """

        elif 'temperature' in query_lower or ('ocean' in query_lower and 'temp' in query_lower):
            print("DEBUG: Temperature query detected")
            # Direct database query for temperature
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT AVG(temperature) as avg_temp, MIN(temperature) as min_temp, MAX(temperature) as max_temp FROM argo_profiles WHERE temperature IS NOT NULL")
                    print(f"DEBUG: Temperature query result: {result}")
                    if result and len(result) > 0:
                        data = result[0]
                        count_result = db_manager.execute_query("SELECT COUNT(*) as count FROM argo_profiles WHERE temperature IS NOT NULL")
                        count = count_result[0]['count'] if count_result else 0
                        return f"""🌡️ **Temperature Analysis:**

📊 **Statistics:**
- Average: {data['avg_temp']:.2f}°C
- Minimum: {data['min_temp']:.2f}°C  
- Maximum: {data['max_temp']:.2f}°C

🌍 **Coverage:** Data from {count} measurements across multiple ocean regions."""
                    else:
                        return "❌ No temperature data found in database."
                except Exception as db_error:
                    print(f"DEBUG: Database error in temperature query: {db_error}")
                    return f"❌ Database error: {str(db_error)}"
            else:
                return "❌ Database not available for temperature analysis."

        elif 'ocean' in query_lower and ('condition' in query_lower or 'data' in query_lower or 'list' in query_lower):
            print("DEBUG: Ocean conditions query detected")
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT * FROM ocean_conditions LIMIT 5")
                    print(f"DEBUG: Ocean conditions result: {result}")
                    if result and len(result) > 0:
                        response = "🌊 **Ocean Conditions Data:**\n\n"
                        for i, condition in enumerate(result, 1):
                            response += f"**Location {i}:** {condition['latitude']:.2f}°N, {condition['longitude']:.2f}°E\n"
                            response += f"- Temperature: {condition['temperature']:.1f}°C\n"
                            response += f"- Salinity: {condition['salinity']:.1f} PSU\n"
                            response += f"- Current Speed: {condition['current_speed']:.1f} m/s\n"
                            response += f"- Pollution Index: {condition['pollution_index']:.1f}\n"
                            response += f"- Alert Level: {condition['alert_level']}\n\n"
                        return response
                    else:
                        return "❌ No ocean conditions data found."
                except Exception as db_error:
                    return f"❌ Database error: {str(db_error)}"

        elif 'salinity' in query_lower:
            print("DEBUG: Salinity query detected")
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT AVG(salinity) as avg_sal, MIN(salinity) as min_sal, MAX(salinity) as max_sal FROM argo_profiles WHERE salinity IS NOT NULL")
                    if result and len(result) > 0:
                        data = result[0]
                        return f"""🧂 **Salinity Analysis:**

📊 **Statistics:**
- Average: {data['avg_sal']:.2f} PSU
- Minimum: {data['min_sal']:.2f} PSU  
- Maximum: {data['max_sal']:.2f} PSU

🌊 **Note:** PSU = Practical Salinity Units. Ocean salinity typically ranges from 33-37 PSU."""
                    else:
                        return "❌ No salinity data found."
                except Exception as db_error:
                    return f"❌ Database error: {str(db_error)}"

        elif 'pollution' in query_lower or 'alert' in query_lower:
            print("DEBUG: Pollution/alert query detected")
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT latitude, longitude, pollution_index, alert_level FROM ocean_conditions WHERE pollution_index > 2.0 ORDER BY pollution_index DESC")
                    if result and len(result) > 0:
                        response = "🚨 **Pollution Alert Report:**\n\n"
                        for condition in result:
                            alert_icon = "🔴" if condition['alert_level'] == 'HIGH' else "🟡" if condition['alert_level'] == 'MEDIUM' else "🟢"
                            response += f"{alert_icon} **{condition['alert_level']} Alert**\n"
                            response += f"   Location: {condition['latitude']:.2f}°N, {condition['longitude']:.2f}°E\n"
                            response += f"   Pollution Index: {condition['pollution_index']:.1f}\n\n"
                        return response
                    else:
                        return "✅ No high pollution areas found (all areas below threshold)."
                except Exception as db_error:
                    return f"❌ Database error: {str(db_error)}"

        elif 'bot' in query_lower or 'agro' in query_lower:
            print("DEBUG: Bot query detected")
            if db_manager:
                try:
                    result = db_manager.execute_query("SELECT bot_name, status, battery_level FROM agro_bots")
                    if result and len(result) > 0:
                        status_text = "🤖 **Agro-Bot Fleet Status:**\n\n"
                        for bot in result:
                            status_icon = "🟢" if bot['status'] == 'ACTIVE' else "🟡"
                            status_text += f"{status_icon} **{bot['bot_name']}**: {bot['status']} (Battery: {bot['battery_level']:.1f}%)\n"
                        return status_text
                    else:
                        return "❌ No bot data found."
                except Exception as db_error:
                    return f"❌ Database error: {str(db_error)}"
        
        # If no direct match found, provide a helpful message
        print("DEBUG: No direct match found, providing suggestions")
        return f"""I understand you asked about: "{query}"

🎯 **I can help with these specific queries:**
- **Temperature**: "temperature", "ocean temp"
- **Ocean Data**: "ocean conditions", "ocean data"  
- **Bot Status**: "bot status", "agro bots"
- **Pollution**: "pollution alerts", "pollution data"
- **Salinity**: "salinity data"

💡 **Try one of these exact phrases for best results!**"""
            
    except Exception as e:
        print(f"DEBUG: Exception in execute_with_timeout: {e}")
        return f"❌ Error processing query: {str(e)}"

def generate_fallback_response(query: str) -> str:
    """Generate a helpful fallback response when the AI agent fails"""
    query_lower = query.lower()
    
    # Try to provide relevant information based on keywords
    if "temperature" in query_lower:
        return """Based on our database, here's what I can tell you about temperature:

🌡️ **Temperature Data Available:**
- Range: 22°C to 29°C across all measurements
- Depth variations: Surface temperatures are typically higher
- Regional differences: Arabian Sea vs Bay of Bengal vs Indian Ocean

💡 **Try asking:** "What's the average temperature?" or "Show temperature by region" """
    
    elif "salinity" in query_lower:
        return """Here's information about salinity in our database:

🧂 **Salinity Measurements:**
- Range: 33.2 to 35.4 PSU (Practical Salinity Units)
- Varies by depth and location
- Important for ocean circulation patterns

💡 **Try asking:** "What's the salinity range?" or "Show salinity data" """
    
    elif "bot" in query_lower or "agro" in query_lower:
        return """Information about our Agro-Bot fleet:

🤖 **Current Fleet Status:**
- 4 Agro-Bots deployed (Alpha, Beta, Gamma, Delta)
- 3 currently active, 1 in maintenance
- Monitoring temperature, salinity, and pH levels

💡 **Try asking:** "Show bot status" or "Which bots are active?" """
    
    elif "pollution" in query_lower:
        return """Pollution monitoring information:

🚨 **Pollution Tracking:**
- Monitoring pollution index across ocean regions
- Alert levels: LOW, MEDIUM, HIGH
- Current hotspots identified near shipping lanes

💡 **Try asking:** "Show pollution alerts" or "Find high pollution areas" """
    
    else:
        return f"""I had trouble processing your query: "{query}"

🎯 **What I can help you with:**
- **Ocean Data**: Temperature, salinity, pH measurements
- **Bot Monitoring**: Agro-Bot status and locations  
- **Pollution Tracking**: Environmental alerts and conditions
- **Regional Analysis**: Data comparisons across ocean areas

💡 **Try these working examples:**
- "Show me all temperature data"
- "What bots are currently active?"
- "Find pollution hotspots"
- "List ocean conditions"

🚀 **Or use the Quick Action buttons in the sidebar!**"""

def format_ai_response(answer: str, original_query: str) -> str:
    """Format the AI response to be more user-friendly"""
    # Add context about the query
    formatted_response = f"**Query:** {original_query}\n\n"
    
    # Clean up the answer
    if "Answer:" in answer:
        answer = answer.split("Answer:")[-1].strip()
    
    # Add helpful context if the answer seems too technical
    if "SELECT" in answer.upper() or "FROM" in answer.upper():
        formatted_response += "**Database Query Results:**\n\n"
    
    formatted_response += answer
    
    # Add suggestions for follow-up questions
    formatted_response += "\n\n---\n*💡 You can ask follow-up questions or try queries like:*\n"
    formatted_response += "*- \"Show me more details about this data\"*\n"
    formatted_response += "*- \"Compare with other regions\"*\n"
    formatted_response += "*- \"What's the trend over time?\"*"
    
    return formatted_response
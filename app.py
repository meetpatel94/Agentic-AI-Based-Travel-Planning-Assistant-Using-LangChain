import streamlit as st
from agent import travel_agent
import json
import pandas as pd
import random
from datetime import datetime
from chatbot import ask_chatbot
# import folium
# from streamlit_folium import st_folium
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
import base64

# ==========================================
# CUSTOM CSS FOR ANIMATIONS & ENHANCEMENTS
# ==========================================

def add_custom_css():
    st.markdown("""
    <style>
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); }
            to { transform: translateX(0); }
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }
        
        /* Glass morphism effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Animated button */
        .stButton > button {
            transition: all 0.3s ease;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            font-weight: bold;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            animation: pulse 0.5s ease-in-out;
        }
        
        /* Animated cards */
        .flight-card, .hotel-card, .place-card {
            animation: fadeIn 0.6s ease-out;
            transition: all 0.3s ease;
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
            border: 1px solid rgba(102, 126, 234, 0.2);
        }
        
        .flight-card:hover, .hotel-card:hover, .place-card:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            background: linear-gradient(135deg, #667eea25 0%, #764ba225 100%);
        }
        
        /* Sidebar styling */
                [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            animation: slideIn 0.5s ease-out;
        }
        
        [data-testid="stSidebar"] * {
            color: white !important;
        }
        
        /* Metrics styling */
        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 15px;
            transition: all 0.3s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
            background: rgba(255,255,255,0.05);
            padding: 10px;
            border-radius: 15px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px;
            padding: 8px 16px;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(102, 126, 234, 0.3);
            transform: translateY(-2px);
        }
        
        /* Progress bar animation */
        .stProgress > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2);
            animation: shimmer 2s infinite;
        }
        
        /* Info boxes */
        .info-box {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 15px;
            padding: 20px;
            color: white;
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Weather cards */
        .weather-card {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            animation: fadeIn 0.6s ease-out;
        }
        
        .weather-card:hover {
            transform: translateY(-5px);
            background: rgba(102, 126, 234, 0.2);
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 10px;
        }
        
        /* Loading spinner */
        .stSpinner > div {
            border-top-color: #667eea !important;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Chart containers */
        .chart-container {
            animation: fadeIn 0.6s ease-out;
            background: rgba(255,255,255,0.05);
            border-radius: 15px;
            padding: 15px;
        }
        
        /* Map container */
        .map-container {
            animation: fadeIn 0.8s ease-out;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI Travel Planner - Smart Journey Planning",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

add_custom_css()

# ==========================================
# LOAD FLIGHT DATA
# ==========================================

with open("data/flights.json", "r") as f:
    flights_data = json.load(f)

# ==========================================
# CREATE ROUTES
# ==========================================

routes = {}
for flight in flights_data:
    source = flight["from"]
    destination = flight["to"]
    if source not in routes:
        routes[source] = []
    if destination not in routes[source]:
        routes[source].append(destination)

source_cities = sorted(routes.keys())

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "animation_trigger" not in st.session_state:
    st.session_state.animation_trigger = False

# ==========================================
# SIDEBAR WITH ENHANCED NAVIGATION
# ==========================================

with st.sidebar:
    # Animated logo/title
    st.markdown("""
    <div style="text-align: center; padding: 0px 0;">
        <h2 style="color: white; margin-top: 0px; font-size: 25px; "> 🌍 AI Travel Planner</h2>
        <p style="color: rgba(255,255,255,0.9); animation: pulse 2s infinite;">Smart Journey Planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.divider()
    
    # Modern navigation menu
    page = option_menu(
        menu_title=None,
        options=["Home", "Search History", "Travel Tips", "Statistics"],
        icons=["house", "clock-history", "lightbulb", "graph-up"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent", "border-radius": "10px!important"},
            "icon": {"color": "white", "font-size": "20px"},
            "nav-link": {
                "color": "white",
                "font-size": "16px",
                "text-align": "left",
                "margin": "5px 0",
                "border-radius": "10px",
                "transition": "all 0.3s ease"
            },
            "nav-link-selected": {
                "background-color": "rgba(255,255,255,0.2)",
                "transform": "translateX(10px)"
            },
        }
    )
    
    
# Travel stats in sidebar
# ==========================================
# AI CHATBOT
# ==========================================

st.sidebar.markdown("---")

st.sidebar.markdown("""
<h3 style='color:white; text-align:center;'>
🤖 AI Travel Assistant
</h3>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="
background:rgba(255,255,255,0.08);
padding:12px;
border-radius:12px;
color:white;
text-align:center;
margin-bottom:10px;
">
Ask me anything about travel!
</div>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "bot_response" not in st.session_state:

    st.session_state.bot_response = ""

# ==========================================
# CHAT FORM
# ==========================================

with st.sidebar.form(
    "chat_form",
    clear_on_submit=True
):

    user_question = st.text_input(
        "✍️ Type your question..."
    )

    submitted = st.form_submit_button(
        "💬 Ask Bot",
        use_container_width=True
    )

# ==========================================
# BOT RESPONSE
# ==========================================

if submitted and user_question:

    bot_response = ask_chatbot(
        user_question
    )

    st.session_state.bot_response = (
        bot_response
    )

# ==========================================
# SHOW RESPONSE
# ==========================================

if st.session_state.bot_response:

    st.sidebar.markdown(
        f"""
        <div style="
        background:rgba(255,255,255,0.12);
        padding:15px;
        border-radius:15px;
        color:white;
        line-height:1.8;
        margin-top:10px;
        margin-bottom:10px;
        ">
        {st.session_state.bot_response.replace(chr(10), "<br>")}
        </div>
        """,
        unsafe_allow_html=True
    )

# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":
    # Hero section with animation
    st.markdown("""
    <div style="text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); border-radius: 30px; margin-bottom: 30px;">
        <h1 style="font-size: 48px; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🌍 AI Travel Planning Assistant
        </h1>
        <p style="font-size: 20px; color: #666;">Plan your smart AI-powered journey with real-time insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Input section with better layout
    st.markdown("### ✈️ Plan Your Journey")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        source = st.selectbox("📍 From", source_cities, help="Select your departure city")
    
    destination_cities = sorted(routes[source])
    with col2:
        destination = st.selectbox("🎯 To", destination_cities, help="Select your destination city")
    
    with col3:
        budget_type = st.selectbox("💰 Budget Type", ["All", "Budget", "Standard", "Luxury"], 
                                  help="Choose your budget preference")
    
    col1, col2 = st.columns(2)
    with col1:
        sort_option = st.selectbox("🔽 Sort Flights By", ["Cheapest", "Highest Price"])
    
    with col2:
        days = st.slider("📅 Duration (Days)", min_value=1, max_value=5, value=3, help="How many days for your trip?")
  
    st.divider()
    
    # Generate button with animation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate = st.button("🚀 Generate Travel Plan", use_container_width=True, type="primary")
    
    # Main generation logic
    if generate:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        
        for i in range(100):
            status_text.text(f"🎯 Planning your trip... {i+1}%")
            progress_bar.progress(i + 1)
            time.sleep(0.01)
        
        status_text.text("✨ Creating your personalized itinerary...")
        
        result = travel_agent(source, destination, days, budget_type)
        
        progress_bar.empty()
        status_text.empty()
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
            st.stop()
        
        # Save to history
        st.session_state.history.append({
            "source": source,
            "destination": destination,
            "days": days,
            "budget": budget_type,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        st.session_state["trip_result"] = result
        if "trip_result" in st.session_state:
             result = st.session_state["trip_result"]

        # Extract data
        flights = result["flights"]
        
        hotels = result["hotels"]
        
        places = result["places"]
        
        weather = result["weather"]
        
        budget = result["budget"]
        
        if "trip_result" in st.session_state:
            result = st.session_state["trip_result"]
            
        # Sort flights
        if sort_option == "Cheapest":
            flights = sorted(flights, key=lambda x: x["price"])
        else:
            flights = sorted(flights, key=lambda x: x["price"], reverse=True)
        
        # Success message with animation
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                    border-left: 5px solid #667eea; 
                    border-radius: 15px; 
                    padding: 20px; 
                    margin: 20px 0;">
            <h3 style="color: #667eea;">✨ Trip Generated Successfully!</h3>
            <p>From <strong>{source}</strong> to <strong>{destination}</strong> • {days} days • {budget_type} Budget</p>
        </div>
        """, unsafe_allow_html=True)
        
        # ==========================================
        # FLIGHTS SECTION
        # ==========================================
        st.markdown('<div class="flight-card">', unsafe_allow_html=True)
        st.header("✈️ Available Flights")
        st.markdown("Compare and choose your perfect flight")
        
        flight_cols = st.columns(2)
        for idx, flight in enumerate(flights):
            with flight_cols[idx % 2]:
                departure = datetime.fromisoformat(flight["departure_time"])
                arrival = datetime.fromisoformat(flight["arrival_time"])
                duration = arrival - departure
                
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.05); border-radius: 15px; padding: 20px; margin: 10px 0;">
                    <h4>✈️ {flight['airline']}</h4>
                    <p>📍 {flight['from']} → {flight['to']}</p>
                    <p>🕒 Departure: {flight['departure_time']}</p>
                    <p>🛬 Arrival: {flight['arrival_time']}</p>
                    <p>⏱️ Duration: {duration}</p>
                    <p style="font-size: 24px; font-weight: bold; color: #667eea;">💰 ₹ {flight['price']:,}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ==========================================
        # HOTELS SECTION
        # ==========================================
        st.markdown('<div class="hotel-card">', unsafe_allow_html=True)
        st.header("🏨 Recommended Hotels")
        st.markdown("Handpicked accommodations for your stay")
        
        hotel_cols = st.columns(2)
        for idx, hotel in enumerate(hotels):
            with hotel_cols[idx % 2]:
                rating = round(random.uniform(3.5, 5.0), 1)
                reviews = random.randint(100, 5000)
                
                stars = "⭐" * hotel['stars']
                
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.05); border-radius: 15px; padding: 20px; margin: 10px 0;">
                    <h4>🏨 {hotel['name']}</h4>
                    <p>{stars} {hotel['stars']}-Star Hotel</p>
                    <p>📍 {hotel['city']}</p>
                    <p>🌟 Rating: {rating}/5.0 ({reviews:,} reviews)</p>
                    <p>💰 ₹ {hotel['price_per_night']:,}/night</p>
                    <p>✨ {', '.join(hotel['amenities'][:3])}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # ==========================================
        # PLACES SECTION WITH GRID
        # ==========================================
        st.header("📍 Must-Visit Attractions")
        st.markdown("Discover the best places in your destination")
        
        place_cols = st.columns(3)
        for idx, place in enumerate(places[:6]):
            with place_cols[idx % 3]:
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.05); border-radius: 15px; padding: 20px; margin: 10px 0; text-align: center;">
                    <div style="font-size: 40px;">🏛️</div>
                    <h4>{place['name']}</h4>
                    <p>🏷️ {place['type']}</p>
                    <p>⭐ Rating: {place['rating']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ==========================================
        # WEATHER SECTION WITH PLOTLY
        # ==========================================
        st.header("🌤️ Weather Forecast")
        
        # Create interactive weather chart
        weather_df = pd.DataFrame({
            'Day': [f'Day {i+1}' for i in range(len(weather))],
            'Temperature (°C)': weather
        })
        
        fig = px.line(weather_df, x='Day', y='Temperature (°C)', 
                     title='Temperature Forecast',
                     line_shape='spline',
                     markers=True)
        fig.update_traces(line_color='#667eea', marker_color='#764ba2', marker_size=10)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', 
                         paper_bgcolor='rgba(0,0,0,0)',
                         font_family="Arial",
                         title_font_size=20)
        st.plotly_chart(fig, use_container_width=True)
        
        # ==========================================
        # INTERACTIVE MAP
        # ==========================================
        st.header("🗺️ Interactive Map")
        st.markdown("Explore attractions and hotels on the map")
        
        city_coordinates = {
            "Delhi": [28.6139, 77.2090],
            "Mumbai": [19.0760, 72.8777],
            "Hyderabad": [17.3850, 78.4867],
            "Bangalore": [12.9716, 77.5946],
            "Goa": [15.2993, 74.1240],
            "Chennai": [13.0827, 80.2707]
        }
        
        map_location = city_coordinates.get(destination, [28.6139, 77.2090])
        travel_map = folium.Map(location=map_location, zoom_start=12)
        
        # Add hotel markers
        for hotel in hotels[:3]:
            lat = map_location[0] + random.uniform(-0.03, 0.03)
            lon = map_location[1] + random.uniform(-0.03, 0.03)
            folium.Marker(
                location=[lat, lon],
                popup=f"🏨 {hotel['name']}",
                tooltip="Hotel",
                icon=folium.Icon(color="blue", icon="hotel", prefix="fa")
            ).add_to(travel_map)
        
        # Add place markers
        for place in places[:5]:
            lat = map_location[0] + random.uniform(-0.05, 0.05)
            lon = map_location[1] + random.uniform(-0.05, 0.05)
            folium.Marker(
                location=[lat, lon],
                popup=place["name"],
                tooltip=place["type"],
                icon=folium.Icon(color="red", icon="camera", prefix="fa")
            ).add_to(travel_map)
        
        st_folium(travel_map, use_container_width=True, height=500, returned_objects=[])
        
        # ==========================================
        # BUDGET SECTION WITH PLOTLY
        # ==========================================
        st.header("💰 Budget Breakdown")
        
        # Create donut chart for budget
        budget_categories = ['Flight', 'Hotel', 'Food', 'Local Transport']
        budget_values = [budget['flight_cost'], budget['hotel_cost'], 
                        budget['food_cost'], budget['local_transport']]
        
        fig = go.Figure(data=[go.Pie(labels=budget_categories, values=budget_values, 
                                     hole=.3,
                                     marker=dict(colors=['#667eea', '#764ba2', '#f093fb', '#f5576c']))])
        fig.update_layout(title="Budget Distribution", 
                         plot_bgcolor='rgba(0,0,0,0)',
                         paper_bgcolor='rgba(0,0,0,0)',
                         annotations=[dict(text=f'Total<br>₹{budget["total_budget"]:,}', 
                                         x=0.5, y=0.5, font_size=20, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("✈️ Flight", f"₹{budget['flight_cost']:,}")
        with col2:
            st.metric("🏨 Hotel", f"₹{budget['hotel_cost']:,}")
        with col3:
            st.metric("🍽️ Food", f"₹{budget['food_cost']:,}")
        with col4:
            st.metric("💰 Total", f"₹{budget['total_budget']:,}")
        
        # ==========================================
        # DAILY ITINERARY
        # ==========================================
        st.header("📅 Daily Itinerary")
        
        tabs = st.tabs([f"Day {i+1} 🗓️" for i in range(min(days, 5))])
        
        for i, tab in enumerate(tabs):
            with tab:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); 
                                border-radius: 15px; padding: 20px;">
                        <h4>🌅 Morning (8:00 AM - 12:00 PM)</h4>
                        <p>• Breakfast at local café</p>
                        <p>• Visit {}</p>
                        <p>• Photography session</p>
                    </div>
                    """.format(places[i % len(places)]['name']), unsafe_allow_html=True)
                    
                with col2:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); 
                                border-radius: 15px; padding: 20px;">
                        <h4>☀️ Afternoon (12:00 PM - 5:00 PM)</h4>
                        <p>• Lunch at traditional restaurant</p>
                        <p>• Explore local markets</p>
                        <p>• Cultural sightseeing</p>
                    </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%); 
                            border-radius: 15px; padding: 20px; margin-top: 20px;">
                    <h4>🌙 Evening (5:00 PM - 10:00 PM)</h4>
                    <p>• Sunset viewing at best spot</p>
                    <p>• Dinner at premium restaurant</p>
                    <p>• Evening entertainment/show</p>
                    <p>• Return to hotel</p>
                </div>
                """, unsafe_allow_html=True)
        
        # ==========================================
        # TRAVEL TIPS SECTION
        # ==========================================
        st.header("💡 Essential Travel Tips")
        
        tip_cols = st.columns(4)
        tips = [
            ("🆔", "Carry Valid ID", "Always keep identification handy"),
            ("🔋", "Power Bank", "Keep devices charged"),
            ("🗺️", "Offline Maps", "Download maps before travel"),
            ("💰", "Emergency Cash", "Carry backup cash")
        ]
        
        for idx, (emoji, title, desc) in enumerate(tips):
            with tip_cols[idx]:
                st.markdown(f"""
                <div style="background: rgba(102, 126, 234, 0.05); border-radius: 15px; padding: 15px; text-align: center;">
                    <div style="font-size: 30px;">{emoji}</div>
                    <h5>{title}</h5>
                    <p style="font-size: 12px;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Download button for itinerary
        st.divider()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            itinerary_text = f"""
            Travel Itinerary for {destination}
            Dates: {datetime.now().strftime('%B %d, %Y')}
            Duration: {days} days
            Budget: {budget_type}
            
            Flights: {len(flights)} options available
            Hotels: {len(hotels)} recommended
            Attractions: {len(places)} places to visit
            
            Total Budget: ₹{budget['total_budget']:,}
            """
            
            st.download_button(
                label="📥 Download Itinerary (PDF)",
                data=itinerary_text,
                file_name=f"itinerary_{destination}_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==========================================
# SEARCH HISTORY PAGE
# ==========================================

elif page == "Search History":
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px;">
        <h1>🕘 Your Travel History</h1>
        <p>Track and manage your past trip plans</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <div style="font-size: 50px;">📭</div>
            <h3>No search history available</h3>
            <p>Start planning your first trip to see your history here!</p>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        history_df = pd.DataFrame(st.session_state.history)
        history_df.index = range(1, len(history_df) + 1)
        
        # Add statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Trips Planned", len(history_df))
        with col2:
            most_frequent = history_df['destination'].mode().iloc[0] if not history_df.empty else "N/A"
            st.metric("Most Visited Destination", most_frequent)
        with col3:
            avg_days = int(history_df['days'].mean()) if not history_df.empty else 0
            st.metric("Average Trip Duration", f"{avg_days} days")
        
        st.divider()
        
        # Display history with better formatting
        for idx, row in history_df.iterrows():
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
                        border-radius: 15px;
                        padding: 20px;
                        margin: 10px 0;">
                <h4>✈️ Trip #{idx}: {row['source']} → {row['destination']}</h4>
                <p>📅 Duration: {row['days']} days • 💰 Budget: {row['budget']} • 👥 Travelers: {row.get('travelers', 1)}</p>
                <p>🕒 Planned on: {row['time']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Clear history button
        if st.button("🗑️ Clear All History", use_container_width=True):
            st.session_state.history = []
            st.rerun()

# ==========================================
# TRAVEL TIPS PAGE
# ==========================================

elif page == "Travel Tips":
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px;">
        <h1>💡 Smart Travel Tips</h1>
        <p>Expert advice for a smooth and memorable journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    tip_categories = {
        "📋 Planning Tips": [
            "Book flights and hotels 2-3 months in advance for best prices",
            "Use price comparison websites to find the best deals",
            "Travel during shoulder season for fewer crowds and lower prices",
            "Create a flexible itinerary with buffer time for unexpected discoveries"
        ],
        "💰 Budget Tips": [
            "Use local public transportation instead of taxis",
            "Eat where locals eat for authentic and affordable meals",
            "Look for free walking tours in major cities",
            "Use travel rewards credit cards for additional savings"
        ],
        "📱 Tech Tips": [
            "Download offline maps before your trip",
            "Use translation apps for non-English speaking destinations",
            "Keep digital copies of important documents in cloud storage",
            "Install local ride-sharing apps for better rates"
        ],
        "🏨 Accommodation Tips": [
            "Read recent reviews before booking hotels",
            "Check hotel locations on maps to ensure convenience",
            "Consider apartment rentals for longer stays",
            "Join hotel loyalty programs for member benefits"
        ],
        "🍽️ Food Tips": [
            "Try street food at busy stalls for the best local flavors",
            "Learn basic food phrases in the local language",
            "Carry snacks for long sightseeing days",
            "Make dinner reservations at popular restaurants in advance"
        ],
        "🚗 Transport Tips": [
            "Research airport to city transport options before arrival",
            "Consider purchasing city transport passes for savings",
            "Use ride-hailing apps rather than street taxis when possible",
            "Check if your destination requires an International Driving Permit"
        ]
    }
    
    for category, tips in tip_categories.items():
        with st.expander(f"📌 {category}", expanded=True):
            for tip in tips:
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px 0;">
                    ✓ {tip}
                </div>
                """, unsafe_allow_html=True)
    
    # Emergency contacts section
    st.divider()
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;">
        <h3>🚨 Emergency Contacts</h3>
        <p>📞 Police: 100 (India)</p>
        <p>🚑 Ambulance: 102 (India)</p>
        <p>🔥 Fire: 101 (India)</p>
        <p>🌍 International Emergency: 112</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FAVORITES PAGE
# ==========================================

elif page == "Favorites":
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px;">
        <h1>❤️ Your Favorite Destinations</h1>
        <p>Save and organize your dream travel spots</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "favorites" not in st.session_state:
        st.session_state.favorites = []
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_favorite = st.text_input("Add a new destination to favorites:")
        if st.button("➕ Add to Favorites"):
            if new_favorite and new_favorite not in st.session_state.favorites:
                st.session_state.favorites.append(new_favorite)
                st.success(f"Added {new_favorite} to favorites!")
                st.rerun()
    
    if st.session_state.favorites:
        st.divider()
        st.subheader("Your Favorite Destinations")
        
        for fav in st.session_state.favorites:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea10 0%, #764ba210 100%);
                            border-radius: 10px;
                            padding: 15px;
                            margin: 5px 0;">
                    🌟 {fav}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("Remove", key=fav):
                    st.session_state.favorites.remove(fav)
                    st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <div style="font-size: 50px;">💔</div>
            <h3>No favorites yet</h3>
            <p>Add destinations you'd love to visit!</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# STATISTICS PAGE
# ==========================================

elif page == "Statistics":
    st.markdown("""
    <div style="text-align: center; padding: 30px 20px;">
        <h1>📊 Travel Statistics</h1>
        <p>Insights from your travel planning journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    if len(st.session_state.history) > 0:
        history_df = pd.DataFrame(st.session_state.history)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Destination popularity chart
            dest_counts = history_df['destination'].value_counts()
            fig = px.pie(values=dest_counts.values, names=dest_counts.index, 
                        title="Most Popular Destinations",
                        color_discrete_sequence=px.colors.sequential.Purples_r)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Budget distribution over time
            budget_counts = history_df['budget'].value_counts()
            fig = px.bar(x=budget_counts.index, y=budget_counts.values,
                        title="Budget Preference Distribution",
                        color=budget_counts.index,
                        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Timeline of trips
        history_df['date'] = pd.to_datetime(history_df['time']).dt.date
        monthly_trips = history_df.groupby(history_df['date']).size()
        
        fig = px.line(x=monthly_trips.index, y=monthly_trips.values,
                     title="Trip Planning Activity Over Time",
                     labels={'x': 'Date', 'y': 'Number of Trips Planned'})
        fig.update_traces(line_color='#667eea', line_width=3, marker_size=10)
        st.plotly_chart(fig, use_container_width=True)
        
        # Additional statistics
        st.divider()
        st.subheader("Quick Insights")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trips", len(history_df))
        with col2:
            st.metric("Unique Destinations", history_df['destination'].nunique())
        with col3:
            st.metric("Most Popular Budget", history_df['budget'].mode().iloc[0] if not history_df.empty else "N/A")
        with col4:
            st.metric("Total Days Planned", history_df['days'].sum())
    else:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <div style="font-size: 50px;">📊</div>
            <h3>No data available yet</h3>
            <p>Start planning trips to see your statistics here!</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div style="text-align: center; padding: 20px; margin-top: 50px; background: linear-gradient(135deg, #667eea05 0%, #764ba205 100%); border-radius: 15px;">
    <p style="color: #666;">🌍 AI Travel Planner | Smart Journey Planning | © 2024</p>
    <p style="font-size: 12px;">Privacy Policy</p>
</div>
""", unsafe_allow_html=True)
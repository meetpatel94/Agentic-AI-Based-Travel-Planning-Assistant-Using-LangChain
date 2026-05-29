# 🌍 AI Travel Planning Assistant

An AI-powered Travel Planning Assistant built using **Python**, **Streamlit**, and **LangChain-inspired agent architecture**. The system helps users plan trips by providing flight recommendations, hotel suggestions, tourist attractions, weather forecasts, budget estimation, interactive maps, and an AI chatbot.

---

## 🚀 Features

### ✈️ Flight Recommendations

* Search available flights between cities
* View airline, departure time, arrival time, duration, and ticket price
* Sort flights by cheapest or highest price

### 🏨 Hotel Recommendations

* Budget Hotels
* Standard Hotels
* Luxury Hotels
* View amenities and hotel ratings

### 📍 Tourist Attractions

* Recommended places based on destination
* Ratings and attraction categories
* Nearby attraction suggestions

### 🌤️ Weather Forecast

* Weather information for selected destination
* Multi-day forecast

### 💰 Budget Planning

* Flight Cost
* Hotel Cost
* Food Cost
* Local Transport Cost
* Total Estimated Budget

### 🗺️ Interactive Travel Map

* Built using Folium
* Displays destination location
* Hotel marker
* Tourist attraction markers

### 🤖 AI Travel Chatbot

* Tourist place recommendations
* Hotel recommendations
* Flight information
* Weather information
* Budget guidance

### 📖 Search History

* Stores previously generated trips
* Displays trip history

### 💡 Travel Tips

* Useful travel recommendations
* Safety and planning suggestions

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Pandas
* JSON
* Folium
* Streamlit-Folium
* Streamlit Option Menu

---

## 📂 Project Structure

```text
AI-Travel-Planner/
│
├── app.py
├── agent.py
├── chatbot.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── flights.json
│   ├── hotels.json
│   └── places.json
│
└── tools/
    ├── flight_tool.py
    ├── hotel_tool.py
    ├── places_tool.py
    ├── weather_tool.py
    └── budget_tool.py
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI-Travel-Planner
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

PowerShell:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application will open at:

```text
http://localhost:8501
```

---

## 🤖 Chatbot Examples

Example Queries:

```text
hi
places
Delhi
hotels
Goa
flights
weather
budget
```

---

## 📊 Dataset

The project uses custom JSON datasets:

### Flights Dataset

Contains:

* Source City
* Destination City
* Airline
* Departure Time
* Arrival Time
* Price

### Hotels Dataset

Contains:

* Hotel Name
* City
* Star Rating
* Price Per Night
* Amenities

### Tourist Places Dataset

Contains:

* Place Name
* City
* Type
* Rating

---

## 🎯 Future Enhancements

* Real-time flight APIs
* Real-time hotel APIs
* Google Maps Integration
* User Authentication
* Booking System
* Personalized Recommendations
* AI Itinerary Generation
* Voice Assistant

---

## 👨‍💻 Author

Meet Patel

AI Travel Planning Assistant Project
Built using Python and Streamlit.

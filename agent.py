from tools.flight_tool import search_flights
from tools.hotel_tool import recommend_hotels
from tools.places_tool import recommend_places
from tools.weather_tool import get_weather
from tools.budget_tool import calculate_budget

# ==========================================
# CITY COORDINATES
# ==========================================

city_coordinates = {
    "Delhi": (28.6139, 77.2090),
    "Goa": (15.2993, 74.1240),
    "Mumbai": (19.0760, 72.8777),
    "Hyderabad": (17.3850, 78.4867),
    "Bangalore": (12.9716, 77.5946),
    "Ahmedabad": (23.0225, 72.5714),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Pune": (18.5204, 73.8567),
    "Jaipur": (26.9124, 75.7873),
    "Surat": (21.1702, 72.8311),
    "Udaipur": (24.5854, 73.7125),
    "Manali": (32.2432, 77.1892),
    "Shimla": (31.1048, 77.1734)
}

# ==========================================
# MAIN AGENT FUNCTION
# ==========================================

def travel_agent(
    source,
    destination,
    days,
    budget_type
):

    # ==========================================
    # FLIGHT SEARCH
    # ==========================================

    flights = search_flights(
        source,
        destination
    )

    # ==========================================
    # HANDLE FLIGHT ERROR
    # ==========================================

    if isinstance(flights, str):

        return {
            "error": f"❌ No flights available from {source} to {destination}"
        }

    # ==========================================
    # SORT FLIGHTS BY PRICE
    # ==========================================

    flights = sorted(
        flights,
        key=lambda x: x["price"]
    )

    # ==========================================
    # TAKE CHEAPEST FLIGHT
    # ==========================================

    flight = flights[0]

    # ==========================================
    # HOTEL RECOMMENDATION
    # ==========================================

    hotels = recommend_hotels(
        destination,
        budget_type
    )

    # ==========================================
    # HANDLE HOTEL ERROR
    # ==========================================

    if isinstance(hotels, str):

        return {
            "error": f"❌ No hotels available in {destination}"
        }

    # ==========================================
    # SORT HOTELS
    # ==========================================

    hotels = sorted(
        hotels,
        key=lambda x: x["price_per_night"]
    )

    # ==========================================
    # TAKE BEST HOTEL
    # ==========================================

    hotel = hotels[0]

    # ==========================================
    # PLACES RECOMMENDATION
    # ==========================================

    places = recommend_places(
        destination
    )

    # ==========================================
    # HANDLE EMPTY PLACES
    # ==========================================

    if isinstance(places, str):

        places = []

    # ==========================================
    # SORT PLACES BY RATING
    # ==========================================

    places = sorted(
        places,
        key=lambda x: x["rating"],
        reverse=True
    )

    # ==========================================
    # WEATHER DATA
    # ==========================================

    latitude, longitude = city_coordinates.get(
        destination,
        (28.6139, 77.2090)
    )

    weather = get_weather(
        latitude,
        longitude
    )

    # ==========================================
    # WEATHER FALLBACK
    # ==========================================

    if isinstance(weather, str):

        weather = [
            30,
            31,
            32,
            29,
            28,
            30,
            31
        ]

    # ==========================================
    # BUDGET CALCULATION
    # ==========================================

    budget = calculate_budget(
        flight["price"],
        hotel["price_per_night"],
        days
    )

    # ==========================================
    # FOOD RECOMMENDATIONS
    # ==========================================

    foods = [

        "Paneer Butter Masala",

        "Biryani",

        "Pizza",

        "Gujarati Thali",

        "Dosa",

        "Street Food",

        "Pasta",

        "South Indian Meals"
    ]

    # ==========================================
    # LOCAL TRANSPORT
    # ==========================================

    transport = [

        "Metro",

        "Taxi",

        "Bus",

        "Rental Bike",

        "Auto Rickshaw"
    ]

    # ==========================================
    # TRAVEL TIPS
    # ==========================================

    travel_tips = [

        "Carry valid ID proof",

        "Keep emergency cash",

        "Use Google Maps offline",

        "Check weather before travel",

        "Book hotels early",

        "Carry medicines",

        "Keep power bank with you"
    ]

    # ==========================================
    # BEST TIME TO VISIT
    # ==========================================

    best_time = "October to March"

    # ==========================================
    # FINAL RESULT
    # ==========================================

    result = {

        "flight": flight,

        "flights": flights,

        "hotel": hotel,

        "hotels": hotels,

        "places": places,

        "weather": weather,

        "budget": budget,

        "foods": foods,

        "transport": transport,

        "travel_tips": travel_tips,

        "best_time": best_time
    }

    return result

# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    result = travel_agent(
        "Hyderabad",
        "Delhi",
        3,
        "Budget"
    )

    print(result)


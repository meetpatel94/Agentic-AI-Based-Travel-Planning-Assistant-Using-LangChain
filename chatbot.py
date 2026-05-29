import json

# ==========================================
# LOAD DATA
# ==========================================

with open("data/places.json", "r") as f:
    places_data = json.load(f)

with open("data/hotels.json", "r") as f:
    hotels_data = json.load(f)

with open("data/flights.json", "r") as f:
    flights_data = json.load(f)

# ==========================================
# CHAT STATE
# ==========================================

chat_state = {
    "mode": None
}

# ==========================================
# CHATBOT FUNCTION
# ==========================================

def ask_chatbot(user_input):

    user_input = user_input.lower().strip()

    # ==========================================
    # GREETING
    # ==========================================

    if user_input in ["hi", "hello", "hey", "start"]:

        chat_state["mode"] = None

        return """
🌍 Which travel information do you need?

✨ I can help with:
📍 Places
🏨 Hotels
✈️ Flights
🌤️ Weather
💰 Budget
"""

    # ==========================================
    # PLACES
    # ==========================================

    if user_input == "places":

        chat_state["mode"] = "places"

        return """
📍 Which city?
🏛️ Delhi
🌆 Mumbai
🏖️ Goa
💎 Hyderabad
🌳 Bangalore
🌊 Chennai
"""

    # ==========================================
    # HOTELS
    # ==========================================

    if user_input == "hotels":

        chat_state["mode"] = "hotels"

        return """
🏨 Which city?
🏛️ Delhi
🌆 Mumbai
🏖️ Goa
💎 Hyderabad
🌳 Bangalore
🌊 Chennai
"""

    # ==========================================
    # PLACES RESPONSE
    # ==========================================

    if chat_state["mode"] == "places":

        city_places = []

        for place in places_data:

            if place["city"].lower() == user_input:

                city_places.append(place)

        if len(city_places) > 0:

            response = f"📍 Best Places in {user_input.title()}\n\n"

            for i, place in enumerate(city_places, 1):

                response += (
                    f"{i}. {place['name']} "
                    f"(⭐ {place['rating']})\n"
                )

            return response

    # ==========================================
    # HOTELS RESPONSE
    # ==========================================

    if chat_state["mode"] == "hotels":

        city_hotels = []

        for hotel in hotels_data:

            if hotel["city"].lower() == user_input:

                city_hotels.append(hotel)

        if len(city_hotels) > 0:

            response = f"🏨 Hotels in {user_input.title()}\n\n"

            for i, hotel in enumerate(city_hotels, 1):

                response += (
                    f"{i}. {hotel['name']} "
                    f"(₹{hotel['price_per_night']}/night)\n"
                )

            return response

    # ==========================================
    # FLIGHTS
    # ==========================================

    if user_input == "flights":

        response = "✈️ Available Flights\n\n"

        for flight in flights_data[:10]:

            response += (
                f"• {flight['from']} → {flight['to']}\n"
                f"  {flight['airline']} | ₹{flight['price']}\n\n"
            )

        return response

    # ==========================================
    # WEATHER
    # ==========================================

    if user_input == "weather":

        return """
🌤️ Weather Information

Weather forecast is available
inside the Travel Planner results page.
"""

    # ==========================================
    # BUDGET
    # ==========================================

    if user_input == "budget":

        return """
💰 Budget Guide

🟢 Budget:
₹10,000 - ₹20,000

🔵 Standard:
₹20,000 - ₹40,000

🟣 Luxury:
₹40,000+
"""

    # ==========================================
    # DEFAULT
    # ==========================================

    return """
🤖 I can help with:
📍 Places
🏨 Hotels
✈️ Flights
🌤️ Weather
💰 Budget

Type:
places
hotels
flights
weather
budget
"""

# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        print("\nBot:")
        print(ask_chatbot(question))
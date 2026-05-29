import json

# ==========================================
# LOAD HOTEL DATA
# ==========================================

with open("data/hotels.json", "r") as f:

    hotels_data = json.load(f)

# ==========================================
# HOTEL RECOMMENDATION FUNCTION
# ==========================================

def recommend_hotels(
    city,
    budget_type="All"
):

    # ==========================================
    # FILTER CITY HOTELS
    # ==========================================

    city_hotels = []

    for hotel in hotels_data:

        if hotel["city"].lower() == city.lower():

            city_hotels.append(hotel)

    # ==========================================
    # NO HOTELS
    # ==========================================

    if len(city_hotels) == 0:

        return "No hotels found"

    # ==========================================
    # ALL HOTELS
    # ==========================================

    if budget_type == "All":

        return city_hotels

    # ==========================================
    # BUDGET FILTER
    # ==========================================

    filtered_hotels = []

    # Budget Hotels

    if budget_type == "Budget":

        for hotel in city_hotels:

            if hotel["price_per_night"] <= 3000:

                filtered_hotels.append(hotel)

    # Standard Hotels

    elif budget_type == "Standard":

        for hotel in city_hotels:

            if (
                hotel["price_per_night"] > 3000
                and
                hotel["price_per_night"] <= 6000
            ):

                filtered_hotels.append(hotel)

    # Luxury Hotels

    elif budget_type == "Luxury":

        for hotel in city_hotels:

            if hotel["price_per_night"] > 6000:

                filtered_hotels.append(hotel)

    # ==========================================
    # IF EMPTY AFTER FILTER
    # ==========================================

    if len(filtered_hotels) == 0:

        filtered_hotels = city_hotels[:3]

    # ==========================================
    # RETURN TOP HOTELS
    # ==========================================

    return filtered_hotels

# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    result = recommend_hotels(
        "Delhi",
        "All"
    )

    print(result)
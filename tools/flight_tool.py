import json

# ==========================================
# LOAD FLIGHT DATA
# ==========================================

with open("data/flights.json", "r") as f:

    flights_data = json.load(f)

# ==========================================
# SEARCH FLIGHTS
# ==========================================

def search_flights(
    source,
    destination
):

    matched_flights = []

    for flight in flights_data:

        if (
            flight["from"].lower() == source.lower()
            and
            flight["to"].lower() == destination.lower()
        ):

            matched_flights.append(flight)

    # ==========================================
    # NO FLIGHTS
    # ==========================================

    if len(matched_flights) == 0:

        return "No flights found"

    # ==========================================
    # SORT BY PRICE
    # ==========================================

    matched_flights = sorted(
        matched_flights,
        key=lambda x: x["price"]
    )

    # ==========================================
    # RETURN TOP 3
    # ==========================================

    return matched_flights[:3]

# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    result = search_flights(
        "Hyderabad",
        "Delhi"
    )

    print(result)
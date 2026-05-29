# ==========================================
# BUDGET CALCULATION
# ==========================================

def calculate_budget(
    flight_price,
    hotel_price,
    days
):

    # ==========================================
    # COSTS
    # ==========================================

    flight_cost = flight_price

    hotel_cost = hotel_price * days

    food_cost = 1000 * days

    local_transport = 500 * days

    total_budget = (

        flight_cost

        +

        hotel_cost

        +

        food_cost

        +

        local_transport
    )

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "flight_cost": flight_cost,

        "hotel_cost": hotel_cost,

        "food_cost": food_cost,

        "local_transport": local_transport,

        "total_budget": total_budget
    }

# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    result = calculate_budget(
        3000,
        4000,
        3
    )

    print(result)


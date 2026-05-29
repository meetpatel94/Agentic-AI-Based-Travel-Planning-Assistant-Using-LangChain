import json


def recommend_places(city):

    with open("data/places.json", "r") as file:
        places = json.load(file)

    matching_places = []

    for place in places:

        if place["city"].lower() == city.lower():
            matching_places.append(place)

    if not matching_places:
        return "No tourist places found."

    return matching_places[:5]


if __name__ == "__main__":

    result = recommend_places("Delhi")

    print(result)
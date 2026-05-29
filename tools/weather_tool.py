import requests


def get_weather(latitude, longitude):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max&timezone=auto"

    response = requests.get(url)

    data = response.json()

    temperatures = data["daily"]["temperature_2m_max"]

    return temperatures


if __name__ == "__main__":

    result = get_weather(
        28.6139,   # Delhi latitude
        77.2090    # Delhi longitude
    )

    print(result)
import requests
from bs4 import BeautifulSoup


class WeatherParser:
    def __init__(self, city: str):
        self.city = city.lower().strip()

        self.url = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-" + self.city
        self._response = requests.get(self.url)
        self._soup = BeautifulSoup(self._response.text, "html.parser")

    def get(self):
        description = self._soup.find("div", class_="description").text.strip()
        today = self._soup.find("p", class_="today-temp").text

        data = {
            "today": today,
            "description": description,
            "days": []
        }

        tabs = self._soup.find("div", class_="tabs")

        days = [tabs.find("div", id=f"bd{index}") for index in range(1, 8)]

        for day in days:
            name = day.find("div", class_="weatherIco").get("title").split(", ")
            weather_icon = day.find("img", class_="weatherImg").get("src")

            #  day_link = day.find("p", class_="day-link").text
            date = day.find("p", class_="date").text
            month = day.find("p", class_="month").text

            temperature = day.find("div", class_="temperature")

            minimum = temperature.find("div", class_="min").find("span").text
            maximum = temperature.find("div", class_="max").find("span").text

            data["days"].append({
                "description": name,
                "weather_icon": weather_icon,
                "date": {
                    #  "day-link": day_link,
                    "day": int(date),
                    "month": month
                },
                "temperature": {
                    "today": today,
                    "max": maximum,
                    "min": minimum
                }
            })

        return data


if __name__ == "__main__":
    weather = WeatherParser(city="Київ")
    print(weather.get())


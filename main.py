import random
import datetime

from reactpy import component, html, use_location, use_state
from reactpy.backend.flask import configure, Options
from reactpy_router import route, simple

from client import WeatherApp
from modules.weather import WeatherParser


months = {
    "серпня": ("Серпень", 8)
}

weekdays = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота", "Неділя"]

weather_colors = [
    ("#4E4FEB", "#068FFF"),
    ("#9681EB", "#6527BE"),
    ("#ACB1D6", "#DBDFEA"),
    ("#A084DC", "#BFACE2"),
    ("#88A47C", "#E6E2C3")
]


@component
def Weather(city: str):
    weather = WeatherParser(city=city)

    data = weather.get()
    day = data["days"][0]

    month = months[day["date"]["month"]]

    timestamp = datetime.datetime.now()
    date = datetime.date(
        year=timestamp.year,
        month=month[1],
        day=timestamp.day
    )

    weekday = date.weekday()

    linear_gradient = random.choice(weather_colors)

    return html.div(
        {
            "class_name": "block",
            "style": {
                "background": f"linear-gradient(45deg, {linear_gradient[0]}, {linear_gradient[1]})",
                "box-shadow": f"box-shadow: 0px 0px 10px {linear_gradient[random.randint(0, 1)]}"
            }
        },
        html.p({"class_name": "day"}, weekdays[weekday]),
        html.p({"class_name": "month"}, month[0]),
        html.p({"class_name": "temperature"}, data["today"]),
        html.div(
            {"class_name": "indicator"},
            html.p("High:"),
            html.p({"class_name": "temp"}, day["temperature"]["max"])
        ),
        html.div(
            {"class_name": "indicator"},
            html.p("Low:"),
            html.p({"class_name": "temp"}, day["temperature"]["min"])
        ),
        html.p({"class_name": "weather"}, ", ".join(day["description"]))
    )


@component
def Main():

    city, set_city = use_state("")
    blocks, set_blocks = use_state([])

    def on_change(e):
        set_city(e["target"]["value"].lower())

    def on_click(e):
        set_blocks([*blocks, Weather(city)])

    return html.div(

        html.div(
            {"class_name": "search"},
            html.input({"on_change": on_change, "class_name": "button"}),
            html.button({"on_click": on_click, "class_name": "button"}, "upsert city")
        ),

        html.div(
            {"class_name": "blocks"},
            blocks
        )
    )


@component
def root():
    location = use_location()

    return simple.router(
        route("/", Main()),
        route("*", html.h1("Missing City 🏙️🔗‍💥")),
    )


app = WeatherApp()


configure(app, root, options=Options(
    head=(
        html.title("Weather App"),
        html.link({"rel": "stylesheet", "href": "static/styles.css"}),
        html.link({"href": "static/favicon.ico", "rel": "shortcut icon", "type": "image/x-icon"})
    ),
    url_prefix="/"
))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)


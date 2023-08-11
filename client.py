from flask import Flask
from whitenoise import WhiteNoise


class WeatherApp(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(__name__, *args, **kwargs)
        self.wsgi_app = WhiteNoise(self.wsgi_app, root="static/", prefix="assets/")

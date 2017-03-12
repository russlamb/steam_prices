from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from price_loader import PriceChecker
my_price_checker = PriceChecker("../../Private/config.ini")
from steam_prices import views
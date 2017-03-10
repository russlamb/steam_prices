from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from price_loader.profit_check import PriceChecker
my_price_checker = PriceChecker("config.ini")
from steam_prices import views
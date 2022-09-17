from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.tickerstream1
import codeitsuisse.routes.tickerstream2
import codeitsuisse.routes.cryptocollapz


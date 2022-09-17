from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.tickerstream1
import codeitsuisse.routes.tickerstream2
import codeitsuisse.routes.cryptocollapz
import codeitsuisse.routes.calendardays
import codeitsuisse.routes.magiccauldrons
import codeitsuisse.routes.quordlekeyboard
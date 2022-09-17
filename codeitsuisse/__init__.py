from flask import Flask
app = Flask(__name__)
import codeitsuisse.routes.square
import codeitsuisse.routes.tickerstream1
import codeitsuisse.routes.tickerstream2
import codeitsuisse.routes.cryptocollapz
import codeitsuisse.routes.calendardays
import codeitsuisse.routes.magiccauldrons
import codeitsuisse.routes.quordlekeyboard
import codeitsuisse.routes.stigwarmup
import codeitsuisse.routes.dns_instantiate
import codeitsuisse.routes.dns_simulator
import codeitsuisse.routes.dns_test
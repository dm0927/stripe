from flask import Flask
from app.routes import paymentintent, home

app = Flask(__name__)

app.register_blueprint(paymentintent.paymentintent)
app.register_blueprint(home.home)
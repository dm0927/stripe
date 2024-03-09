from app import app
from dotenv import dotenv_values

config = dotenv_values(".env")

app.config['STRIPE_SECRET_KEY'] = config['STRIPE_SECRET_KEY']

if __name__ == '__main__':
    app.run(debug=True)
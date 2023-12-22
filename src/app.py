import os

from dash_app import app
from dotenv import load_dotenv
from flask import Flask
from utils.models import login_manager, mongo

load_dotenv(override=True)

server = Flask(__name__)
server.config.update(SECRET_KEY=os.environ.get("SECRET_KEY"))
server.config.update(MONGO_URI=os.environ.get("DB_ECONODATA"))

mongo.init_app(server)
login_manager.init_app(server)
app.init_app(server)


if __name__ == "__main__":
    # app.run(debug=True)
    server.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

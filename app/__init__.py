from flask import Flask
from app.extensions import mongo  # Import mongo from extensions
from .routes import bp  # Import routes after defining the app
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable is not set.")

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI

    # Initialize MongoDB
    mongo.init_app(app)

    # Register blueprint for routes
    app.register_blueprint(bp)

    return app

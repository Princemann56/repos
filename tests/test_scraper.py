import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, mongo  # Import the Flask app factory and MongoDB instance
from app.scraper import scrape_reviews  # Import scrape_reviews from scraper.py

def check_database():
    reviews = mongo.db.reviews.find()  # Retrieve all reviews from MongoDB
    for review in reviews:
        print(f"Date: {review['date']}, Content: {review['content']}, Category: {review['category']}")

if __name__ == "__main__":
    # Initialize and push the Flask app context
    app = create_app()
    with app.app_context():
        scrape_reviews(mongo)  # Pass mongo to scrape_reviews
        check_database()  # Check the database and print the reviews

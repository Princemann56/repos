from flask import Blueprint, request, jsonify, render_template
from datetime import datetime, timedelta
from app.extensions import mongo
from app.utils import generate_daily_summary  # Import the summary function

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        # Extract and parse query parameters
        date_str = request.args.get('date')
        category = request.args.get('category')

        # Parse the selected date
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return jsonify({"error": "Invalid date format. Expected YYYY-MM-DD."}), 400
        
        # Calculate the 7-day rolling period
        start_date = selected_date - timedelta(days=6)
        end_date = selected_date

        # Retrieve all reviews for the selected day and category
        try:
            daily_reviews = list(mongo.db.reviews.find({
                "date": selected_date.strftime('%Y-%m-%d'),
                "category": category
            }))
            daily_review_count = len(daily_reviews)
        except Exception as e:
            print(f"Error retrieving daily reviews from MongoDB: {e}")
            return jsonify({"error": "Error retrieving daily reviews."}), 500

        # Retrieve review counts for each day in the 7-day period for the selected category
        trend_data = []
        try:
            for i in range(7):
                day = start_date + timedelta(days=i)
                count = mongo.db.reviews.count_documents({
                    "date": day.strftime('%Y-%m-%d'),
                    "category": category
                })
                trend_data.append({
                    "date": day.strftime('%Y-%m-%d'),
                    "count": count
                })
        except Exception as e:
            print(f"Error calculating 7-day trend data: {e}")
            return jsonify({"error": "Error calculating trend data."}), 500

        # Format and return response data
        response = {
            "selected_date": selected_date.strftime('%Y-%m-%d'),
            "category": category,
            "daily_count": daily_review_count,
            "trend": trend_data,
            "reviews": [{"date": r["date"], "content": r["content"]} for r in daily_reviews]
        }

        return jsonify(response)

    except Exception as e:
        print(f"Unexpected error in get_reviews: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@bp.route('/daily-summary', methods=['GET'])
def daily_summary():
    # Get the date parameter from the request, default to today's date if not provided
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    
    # Retrieve or generate the summary for the specified date
    summary = mongo.db.daily_summaries.find_one({"date": date_str})
    
    # If summary does not exist, generate it for the date
    if not summary:
        summary = generate_daily_summary(mongo, date_str)
    
    # Return the summary as JSON
    return jsonify(summary)

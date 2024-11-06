from datetime import datetime
from collections import Counter

def generate_daily_summary(mongo, target_date=None):
    """
    Generate a summary of reviews for a specific day.
    If no target_date is provided, it defaults to today's date.
    
    Parameters:
    - mongo: MongoDB client instance
    - target_date: date for the summary in 'YYYY-MM-DD' format, optional
    """
    # Default to today's date if no date is specified
    if target_date is None:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    # Fetch all reviews for the target date
    reviews_for_day = list(mongo.db.reviews.find({"date": target_date}))
    
    # If no reviews found for the day, return an empty summary
    if not reviews_for_day:
        print(f"No reviews found for {target_date}.")
        return {"date": target_date, "total_reviews": 0, "category_counts": {}}
    
    # Count reviews by category
    categories = [review["category"] for review in reviews_for_day]
    category_counts = dict(Counter(categories))
    
    # Total reviews for the day
    total_reviews = len(reviews_for_day)
    
    # Prepare the summary
    daily_summary = {
        "date": target_date,
        "total_reviews": total_reviews,
        "category_counts": category_counts
    }
    
    print(f"Daily summary for {target_date}:", daily_summary)
    return daily_summary

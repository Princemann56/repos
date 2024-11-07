from app import create_app, mongo
from flask_apscheduler import APScheduler
from app.scraper import scrape_reviews
from app.utils import generate_daily_summary  # Import the summary function
from datetime import datetime
from flask_cors import CORS  # Import CORS
import os

app = create_app()
CORS(app)  # Enable CORS for all routes

scheduler = APScheduler()

# Scheduled task to scrape reviews every 24 hours
@scheduler.task('interval', id='scrape_reviews', hours=24)
def scheduled_scrape_task():
    with app.app_context():
        scrape_reviews(mongo)

# Scheduled task to generate a daily summary at 11:59 PM
@scheduler.task('cron', id='generate_daily_summary', hour=23, minute=59)
def scheduled_daily_summary():
    with app.app_context():
        target_date = datetime.now().strftime('%Y-%m-%d')
        generate_daily_summary(mongo, target_date)

scheduler.init_app(app)
scheduler.start()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)

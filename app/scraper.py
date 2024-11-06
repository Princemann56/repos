from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

GAME_URL = "https://play.google.com/store/apps/details?id=com.superplaystudios.dicedreams"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")

# Define label mappings (adjust based on your needs)
LABELS = ["Bugs", "Crashes", "Complaints", "Praises", "Other"]

def classify_review(content):
    # Tokenize and prepare input for the model
    inputs = tokenizer(content, return_tensors="pt", truncation=True, padding=True)
    
    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Get the predicted label
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted_label = np.argmax(probabilities[0].cpu().numpy())
    
    # Return the predicted category
    return LABELS[predicted_label]

def scrape_reviews(mongo):
    # Set up Selenium with Chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(GAME_URL)

    # Click "See all reviews" button
    try:
        load_more_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'See all reviews')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", load_more_button)
        print("Clicked on 'See all reviews' button")
    except Exception as e:
        print("Failed to find or click the 'See all reviews' button:", e)
        driver.quit()
        return

    # Incremental retries to load more reviews
    retries = 10  # Number of retry attempts
    for attempt in range(retries):
        try:
            # Scroll to the bottom to trigger more comments loading
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for content to load

            # Check for the presence of review elements
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "h3YV2d"))
            )
            print("Reviews loaded successfully")
            break  # Exit loop if reviews are found
        except TimeoutException: # type: ignore
            print(f"Attempt {attempt + 1} of {retries}: Retrying...")
            time.sleep(2)
    else:
        print("Failed to load reviews after retries.")
        driver.quit()
        return

    # Scrape all reviews and dates after loading more comments
    reviews = driver.find_elements(By.CLASS_NAME, 'h3YV2d')
    dates = driver.find_elements(By.CLASS_NAME, 'bp9Aid')
   
    # Iterate over reviews and save each to MongoDB
    for review_elem, date_elem in zip(reviews, dates):
        content = review_elem.text
        date_str = date_elem.text
        try:
            date = datetime.strptime(date_str, '%B %d, %Y')
        except ValueError:
            continue  # Skip review if date parsing fails

        # Classify and store the review in MongoDB
        category = classify_review(content)
        new_review = {
            "date": date.strftime('%Y-%m-%d'),
            "content": content,
            "category": category
        }
        
        # Insert into MongoDB collection if review doesn't already exist
        if not mongo.db.reviews.find_one({"content": content}):
            mongo.db.reviews.insert_one(new_review)
            print(f"Saved review - Date: {new_review['date']}, Category: {new_review['category']}, Content: {new_review['content']}")

    driver.quit()

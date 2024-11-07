# Segwise Review Monitor

Segwise Review Monitor is a full-stack application designed to monitor and classify reviews for the mobile game "Dice Dreams." The app scrapes reviews, classifies them using a machine learning model, and provides daily summaries. The backend is containerized with Docker, uses MongoDB for data storage, and is deployed on Render.

---

## Table of Contents

- [Project Features](#project-features)
- [Tech Stack](#tech-stack)
- [Setup and Installation](#setup-and-installation)
- [Environment Variables](#environment-variables)
- [Docker Deployment](#docker-deployment)
- [Render Deployment](#render-deployment)
- [API Endpoints and Sample Requests](#api-endpoints-and-sample-requests)
- [Cost Estimation](#cost-estimation)
- [Collaborators](#collaborators)
- [License](#license)

---

## Project Features

1. **Review Scraping**: Automatically scrapes reviews from the Google Play Store.
2. **Sentiment Classification**: Classifies reviews into categories (Bugs, Crashes, Complaints, Praises, Other) using a DistilBERT model.
3. **Daily Summary**: Generates a daily summary of reviews.
4. **Frontend Interface**: Displays review summaries and trends, allowing users to view individual reviews.

---

## Tech Stack

- **Backend**: Python, Flask, Flask-APScheduler, MongoDB
- **Machine Learning**: Hugging Face Transformers (DistilBERT model)
- **Containerization**: Docker
- **Deployment**: Render

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB
- Docker (for containerization)
- Git (for version control)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/princemann56/segwise.git
   cd segwise

2. **Create a virtual environment:**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Run the Backend Application:**
   ```bash
   python run.py

# Docker Deployment

## To deploy the application using Docker:

1. **Build the Docker Image:**
    ```bash
    docker build -t your-dockerhub-username/segwise-review-monitor .
 2. **Run the Docker Container:**
    ```bash
    docker run -p 5000:5000 your-dockerhub-username/segwise-review-monitor

3. **Push the Docker Image to Docker Hub (if deploying to the cloud):**
   ```bash
   docker push your-dockerhub-username/segwise-review-monitor

# Render Deployment
[deployed link via render](https://segwise-3.onrender.com/)

## API Endpoints and Sample Requests

The backend exposes the following API endpoints:

GET /reviews - Fetches reviews for a specified date and category.

Parameters:
- date (string, required): Date in YYYY-MM-DD format
- category (string, required): Category of review (e.g., Bugs, Crashes)




## Cost Estimation

For running the system in production 24/7 for 30 days, with an estimated 5 queries per day:

1. **Render Free Tier**:
   - Render's free tier provides 512 MB of memory and supports up to 750 hours per month, which covers a full month of continuous uptime.
   - Cost: $0, as long as memory usage stays within the free tier limit.

2. **MongoDB Atlas Free Tier**:
   - MongoDB Atlas offers 500 MB of storage on the free tier, which should be sufficient for a month of review data.

**Total Estimated Cost**: **$0** (using Render and MongoDB Atlas free tiers)

---

## Collaborators

- **shobhit@segwise.ai**
- **bhumit@segwise.ai**


# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that the app runs on
EXPOSE 5000

# Define environment variables (optional, replace with actual values if needed)
ENV MONGO_URI=mongodb+srv://Prince:fWJwG4uunAgMsdmg@prince.oo1aoqb.mongodb.net/segwise

# Run the command to start the Flask app
CMD ["python", "run.py"]

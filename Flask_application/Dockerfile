# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install --no-cache-dir flask numpy tensorflow pillow 

# Expose the port Flask runs on
EXPOSE 5000

# Command to run your Flask application
CMD ["python", "app.py"]

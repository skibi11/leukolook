# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies, including wget to download the model
RUN apt-get update && apt-get install -y \
    wget \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the directory for the model
RUN mkdir -p /app/api/models

# Use wget to download the model from your GitHub Release into the correct directory
# !!! REPLACE THE URL WITH THE ONE YOU COPIED !!!
RUN wget -O /app/api/models/MobileNetV1_best.keras "https://github.com/skibi11/leukolook-backend/releases/download/v1.0/MobileNetV1_best.keras"

# Copy the rest of your application's code into the container
COPY . .

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose port 8080 for Render
EXPOSE 8080

# Set the entrypoint script as the container's main command
CMD ["/app/entrypoint.sh"]
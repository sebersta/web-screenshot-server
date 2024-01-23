# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install dependencies for Chromium and ChromeDriver
RUN apt-get update && apt-get install -y wget gnupg2 \
    && apt-get install -y chromium chromium-driver  \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirekments.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "./app.py"]

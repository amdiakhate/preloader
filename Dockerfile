# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the start script into the container
COPY start.sh /start.sh

# Make the start script executable
RUN chmod +x /start.sh

# Run the start script when the container launches
ENTRYPOINT ["/start.sh"]

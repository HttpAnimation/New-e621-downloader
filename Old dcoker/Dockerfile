# Use an official Python runtime as a parent image
FROM python:3.8

# Install wget for downloading images
RUN apt-get update && \
    apt-get install -y wget && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for the PHP status page
EXPOSE 80

# Run the Python script and start the PHP server for the status page
CMD ["bash", "-c", "python app.py & php -S 0.0.0.0:80"]

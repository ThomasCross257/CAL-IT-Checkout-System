# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Create a directory for storing uploaded files
RUN mkdir /uploads

# Set the permissions for the uploads directory
RUN chmod 777 /uploads

# Expose port 5000 for the Flask application
EXPOSE 5000

# Mount the uploads directory as a volume
VOLUME /uploads

# Run the command to start the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
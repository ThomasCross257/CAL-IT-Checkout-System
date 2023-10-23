# Use an official Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for storing uploaded files
RUN mkdir /uploads

# Set the permissions for the uploads directory
RUN chmod 777 /uploads

# Copy the rest of the application code into the container at /app
COPY . .

# Create and activate the Python virtual environment
RUN python -m venv venv
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate

# Set the environment variable for Flask
ENV FLASK_APP=main.py
ENV FLASK_ENV=production


# Expose port 8000 for the Flask application
EXPOSE 8000

# Mount the uploads directory as a volume
VOLUME /uploads

#Mount database as a volume
VOLUME /instance

# Run the command to start the Flask application inside the virtual environment
CMD ["gunicorn", "-w", "1", "--threads", "4", "-b", "0.0.0.0:8000", "main:app"]

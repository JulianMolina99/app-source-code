# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory within the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the necessary dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container's /app directory
COPY . .

# Expose port 8000 for the Uvicorn server
EXPOSE 8000

# Set the command to launch the application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
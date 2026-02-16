# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY main.py .
COPY services/ services/
COPY convert_data.py .
COPY download_data.py .

# Download and process data during build
# This will result in a larger image if not cleaned up properly, currently download_data.py handles cleanup
RUN python download_data.py

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for API Token (should be overridden in deployment)
ENV INTERNAL_API_TOKEN=""

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

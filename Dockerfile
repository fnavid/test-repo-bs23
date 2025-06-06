# Use official Python runtime as a lightweight base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Install system dependencies for faster builds and security
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app source code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

ENV APP_VERSION = dev

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

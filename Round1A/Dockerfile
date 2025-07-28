# Use Python 3.11 slim image for AMD64 architecture
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for PyMuPDF
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ ./src/
COPY main.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Make the main script executable
RUN chmod +x main.py

# Set the default command
CMD ["python", "main.py"]

# Use an official lightweight Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies (for subprocess TTS tools)
RUN apt-get update && apt-get install -y \
    git \
    espeak \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirement files
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app and model/config files
COPY . .

# Expose the API port
EXPOSE 8000

# Run FastAPI app using uvicorn automatically inside Docker
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

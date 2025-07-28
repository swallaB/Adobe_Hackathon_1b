# Use a more complete base image to reduce build time
FROM python:3.10-bullseye

# Set working directory
WORKDIR /app

# Preinstall system packages required for faiss, PyMuPDF, tesseract, poppler
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libglib2.0-0 \
    libgl1-mesa-glx \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run script
CMD ["python", "main.py"]
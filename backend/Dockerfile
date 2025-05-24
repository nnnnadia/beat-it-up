# Use the official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN apt-get update && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/* && \
  apt-get update && \
  apt-get install -y --fix-missing tesseract-ocr tesseract-ocr-por && \
  rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code
COPY app/ ./app/

# Set PYTHONPATH so 'app' is always importable
ENV PYTHONPATH=/app

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

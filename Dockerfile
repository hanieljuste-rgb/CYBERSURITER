# Use Python 3.12
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY web_app.py .
COPY README.md .

# Expose port
EXPOSE 8888

# Set environment variables
ENV PORT=8888
ENV RAILWAY_ENVIRONMENT=production

# Run the application
CMD ["gunicorn", "web_app:app", "--bind", "0.0.0.0:8888", "--workers", "2"]

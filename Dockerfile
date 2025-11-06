# Use Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Expose port for Render
EXPOSE 8000

# Start the app
CMD ["gunicorn", "amazonPriceTracker.wsgi:application", "--bind", "0.0.0.0:8000"]

# Use an official lightweight Python image as the base
FROM python:3.9-slim

# Establish the working directory inside the container
WORKDIR /app

# Copy the dependencies file and install requirements safely
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the actual application package into the container
COPY service/ service/

# Create a non-root system user for security enforcement
RUN useradd -u 1000 theia && chown -R theia:theia /app
USER theia

# Expose the internal container application port
EXPOSE 8080

# Configure the service entry point using gunicorn
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]

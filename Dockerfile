FROM python:3.9-slim

WORKDIR /app

# Copy and install dependencies first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary application files into the container image
COPY service/ service/

# Establish security privileges for non-root context execution
RUN useradd -u 1001 theia && chown -R theia:theia /app
USER theia

EXPOSE 8080

CMD ["gunicorn", "--bind=0.0.0.0:8080", "--log-level=info", "service:app"]

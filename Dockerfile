# Hong Bien RSS Tool - Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY rss_telegram.py .
COPY setup.py .
COPY config.json.example .

# Create volume mount points
VOLUME ["/app/config.json", "/app/rss_state.sqlite3"]

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Health check (optional)
HEALTHCHECK --interval=5m --timeout=10s --start-period=30s \
  CMD python -c "import sys; sys.exit(0)"

# Run the bot
CMD ["python", "-u", "rss_telegram.py"]

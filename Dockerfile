FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl ca-certificates build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -d /home/django -s /bin/bash django

# Set work directory
WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --locked

# Copy project files
COPY . .

# Create directories and set permissions
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Default command
CMD ["uv", "run", "uvicorn", "proposify_ai.asgi:application", \
     "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4"]

# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Prevents Python from writing .pyc files and using stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy metadata first (for caching)
COPY pyproject.toml ./

# Copy backend code so setuptools can find it
COPY . .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip \
  && pip install ".[deploy]"

# Expose port for Gunicorn
EXPOSE 8000

# Start the app with 2 Uvicorn workers through Gunicorn
CMD ["gunicorn", "backend.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000"]

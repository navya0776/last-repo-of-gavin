# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Prevents Python from writing .pyc files and using stdout buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /app

# Copy metadata first (for caching)
COPY pyproject.toml ./

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
     gcc \
     libpq-dev \
     postgresql-client \
  && rm -rf /var/lib/apt/lists/*


# Copy backend code so setuptools can find it
COPY . .

# Upgrade pip and install dependencies
RUN chmod +x /app/scripts/entrypoint.sh

RUN pip install --upgrade pip \
  && pip install ".[deploy]"

# Expose port for Gunicorn
EXPOSE 8000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Start the app with 2 Uvicorn workers through Gunicorn
CMD ["gunicorn", "backend.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "2", "-b", "0.0.0.0:8000"]

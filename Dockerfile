# Use Playwright noble with Python 3.12
FROM mcr.microsoft.com/playwright/python:v1.57.0-noble

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction \
    && apt-get update && apt-get install -y xvfb

# Copy the rest of the project
COPY . .

# Ensure scripts are executable
RUN chmod +x run_tests.sh

# Default entrypoint
ENTRYPOINT ["pytest"]

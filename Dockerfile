# Use the official image as a parent image.
# Pin to 3.12-slim — current Python LTS, matches the project's target runtime.
# Update this when you upgrade your local Python version.
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install dependencies first (separate layer — cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (.dockerignore excludes .venv, .flaskenv, .git, etc.)
COPY . .

# Expose the application port
EXPOSE 5000

# wsgi.py at the project root exports `app` for gunicorn
ENV FLASK_APP=wsgi.py

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]

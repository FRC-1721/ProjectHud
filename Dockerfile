# Use the official Python slim image as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install dependencies globally
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the app code to the container
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Bake the git commit into the env
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

# Healthcheck to ensure the service is up
# HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
#     CMD curl --fail http://localhost:5000/ || exit 1

# Run Gunicorn without virtual environment
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "-t", "120", "wsgi:app"]

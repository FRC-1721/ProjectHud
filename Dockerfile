FROM python:3.12-slim

# Authors
LABEL authors="31870999+KenwoodFox@users.noreply.github.com"

# Set the name of our app
ARG APP_NAME=project-hud
ENV APP_NAME=${APP_NAME}

# Get the current git version
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT

# App home
ARG HOME="/app"
ENV HOME=${HOME}

# Upgrade pip
RUN pip install --upgrade pip --no-cache-dir

# Set workdir
WORKDIR ${HOME}

# Add any packages we need
# RUN apt update && apt install python-dev-is-python3 -y

# Copy the Pipfile and Pipfile.lock into the container at /app
COPY Pipfile Pipfile.lock /app/

# Install any needed packages specified in Pipfile
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy in everything else
ADD . ${HOME}

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

# Run the app when the container launches
CMD ["pipenv", "run", "gunicorn", "--bind", "0.0.0.0:5000", "run:app", "--worker-class", "eventlet", "--workers", "1", "--preload"]

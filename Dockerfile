# Flask Dockerfile
ARG PYTHON_VERSION=3.12.5

# Use an official Python runtime as a parent image
FROM python:${PYTHON_VERSION}-slim as base
#FROM python:3.10-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/nonexistent" \
#     --shell "/sbin/nologin" \
#     --no-create-home \
#     --uid "${UID}" \
#     appuser

# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --home "/home/appuser" \
#     --shell "/sbin/nologin" \
#     --uid "${UID}" \
#     appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
# RUN --mount=type=cache,target=/root/.cache/pip \
#     --mount=type=bind,source=requirements.txt,target=requirements.txt \
#     python -m pip install -r requirements.txt
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install -r requirements.txt

# Install the necessary Python packages
#RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update -y 
#&& apt-get install -y libpq-dev
RUN apt-get install sudo nano vim -y

# Copy the current directory contents into the container
COPY . /app

#RUN chown -R appuser:appuser /app/*
# Ensure the database file has the correct permissions
#RUN chmod 777 /app/games.db

# Switch to the non-privileged user to run the application.
#USER appuser

EXPOSE 5000

# Run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app", "--workers", "4"]

# Set Flask environment variables
#ENV FLASK_APP=app.py
#ENV FLASK_ENV=development

# Run the Flask app
#CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

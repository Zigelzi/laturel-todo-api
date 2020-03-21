# Pull official base image
FROM python:3.8.1-slim-buster

# Set work directory
WORKDIR /usr/src/todo-api

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/todo-api/requirements.txt
RUN pip install -r requirements.txt

# Copy the project
COPY . /usr/src/todo-api/
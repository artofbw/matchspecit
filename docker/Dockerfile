# Use an official Python runtime as a parent image
FROM python:3.9.9

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1  # This prevents Python from writing out pyc files
ENV PYTHONUNBUFFERED 1  # This keeps Python from buffering stdin/stdout

# Adding app directory to make absolute filepaths consistent across services
WORKDIR /app

# installing netcat (nc) since we are using that to listen to postgres server in entrypoint.sh
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements /app/requirements
COPY requirements.txt /app

RUN pip install --upgrade pip -r requirements.txt

# Make port 8000 available for the app
EXPOSE 8000

CMD gunicorn matchspecit.core.wsgi:application -w 2 -b 0.0.0.0:8000 --reload

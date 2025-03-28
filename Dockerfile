FROM python:3.12
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# No need to EXPOSE a specific port, Heroku will handle this

# Use gunicorn directly with dynamic port
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
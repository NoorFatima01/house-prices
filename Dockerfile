FROM python:3.12
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app
COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
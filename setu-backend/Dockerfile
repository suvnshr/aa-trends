FROM python:3.11-slim-bookworm

COPY . /app
WORKDIR /app

# Install the requirements
RUN pip3 install -r requirements.txt

# Run the flask server using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
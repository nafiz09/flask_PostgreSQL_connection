FROM python:3.9-slim

WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED 1

CMD ["python", "app.py"]

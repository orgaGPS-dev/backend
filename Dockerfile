# Basis-Image
FROM python:3.9-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Systemabhängigkeiten installieren
RUN apt-get update && apt-get install -y gcc

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Statische Dateien sammeln
RUN python manage.py collectstatic --noinput

# Gunicorn installieren
RUN pip install gunicorn

# Standard-Port für die Anwendung
EXPOSE 8000

# Startbefehl für Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "orgagps.wsgi:application"]

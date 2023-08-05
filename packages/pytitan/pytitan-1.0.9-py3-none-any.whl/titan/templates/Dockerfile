#gunicorn-flask
FROM  ohohok/python3.7.1:v1

ENV FLASK_ENV production
RUN mkdir -p /app && mkdir -p /app/instance && touch /app/instance/config.py
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt --no-cache-dir


EXPOSE 8080
# Start gunicorn
CMD ["gunicorn", "--config", "gunicorn_config.py","wsgi:app"]
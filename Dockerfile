FROM python:3.12-slim

WORKDIR /app

COPY app.py test_app.py ./

ENV APP_VERSION=v1

EXPOSE 8000

CMD ["python", "app.py"]

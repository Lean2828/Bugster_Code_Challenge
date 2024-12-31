FROM python:3.10-slim

WORKDIR /app

COPY ./services/event_service/. /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./shared_module /app/

COPY ./.env /app/.env

ENV PYTHONPATH=/app:/app/shared_module

RUN ls -R /app > /dev/stdout

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

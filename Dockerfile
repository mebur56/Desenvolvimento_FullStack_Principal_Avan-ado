FROM python:3.14

WORKDIR /app

COPY src/ ./src

RUN pip install --no-cache-dir -r src/requirements.txt

ENV FLASK_APP=src/app.py
ENV PYTHONPATH=/app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
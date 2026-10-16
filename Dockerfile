FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CIVICSHIFT_ENV=container \
    CIVICSHIFT_DB=/app/var/civicshift.db

WORKDIR /app

RUN addgroup --system civicshift && adduser --system --ingroup civicshift civicshift
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/var && chown -R civicshift:civicshift /app

USER civicshift
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=2)"

CMD ["python", "-m", "uvicorn", "services.api.civicshift.main:app", "--host", "0.0.0.0", "--port", "8000"]

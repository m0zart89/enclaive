FROM python:3.12-alpine AS builder

WORKDIR /build

RUN apk add --no-cache gcc musl-dev libffi-dev

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir fastapi==0.136.3 uvicorn==0.48.0 prometheus-client==0.25.0

FROM python:3.12-alpine

WORKDIR /code

RUN addgroup -S -g 10001 appgroup && adduser -S -u 10001 -G appgroup appuser

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY --chown=appuser:appgroup . /code

USER appuser

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/healthz')"

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

import json
import os

from fastapi import FastAPI, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

MY_COUNTER = Counter("app_custom_events_total", "Test counter")

@app.get("/healthz")
async def healthz():
    MY_COUNTER.inc()
    return {"SYS_ENV": os.getenv('SYS_ENV')}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
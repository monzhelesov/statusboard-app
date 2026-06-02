from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest
from datetime import datetime
import os

app = FastAPI(title="StatusBoard API")

REQUEST_COUNT = Counter("api_requests_total", "Total requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("api_request_duration_seconds", "Request latency", ["endpoint"])

@app.get("/api/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/services")
def get_services():
    services = [
        {"name": "API Gateway", "status": "operational", "uptime": "99.98%"},
        {"name": "Database", "status": "operational", "uptime": "99.95%"},
        {"name": "Cache", "status": "degraded", "uptime": "98.50%"},
        {"name": "Queue", "status": "operational", "uptime": "99.99%"},
    ]
    return {"services": services, "checked_at": datetime.utcnow().isoformat()}

@app.get("/api/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.middleware("http")
async def track_requests(request, call_next):
    with REQUEST_LATENCY.labels(endpoint=request.url.path).time():
        response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    return response

import random
import time

from flask import Flask
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUESTS = Counter(
    "demo_http_requests_total",
    "Total HTTP requests",
    ["endpoint", "status"],
)

LATENCY = Histogram(
    "demo_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)

IN_FLIGHT = Gauge(
    "demo_http_requests_in_flight",
    "Current in-flight HTTP requests",
)

ERRORS = Counter(
    "demo_http_errors_total",
    "Total HTTP 5xx errors",
    ["endpoint"],
)


def handle(endpoint, error_rate=0.05):
    IN_FLIGHT.inc()
    start = time.time()
    try:
        time.sleep(random.uniform(0.01, 0.4))
        if random.random() < error_rate:
            REQUESTS.labels(endpoint=endpoint, status="500").inc()
            ERRORS.labels(endpoint=endpoint).inc()
            return "error", 500
        REQUESTS.labels(endpoint=endpoint, status="200").inc()
        return "ok", 200
    finally:
        LATENCY.labels(endpoint=endpoint).observe(time.time() - start)
        IN_FLIGHT.dec()


@app.route("/api/users")
def users():
    return handle("/api/users")


@app.route("/api/orders")
def orders():
    return handle("/api/orders", error_rate=0.08)


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


@app.route("/")
def index():
    return "demo-api up — try /api/users, /api/orders, /metrics\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

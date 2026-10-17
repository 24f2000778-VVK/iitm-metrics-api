import time
import uuid
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, Response

APP_EMAIL = "24f2000778@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-j3abmr.example.com"
app = FastAPI(title="CORS-Aware Metrics API")

@app.middleware("http")
async def required_headers_and_cors(request: Request, call_next):
    started = time.perf_counter()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("origin")

    if request.method == "OPTIONS" and request.url.path == "/stats":
        if origin != ALLOWED_ORIGIN:
            response = JSONResponse(status_code=403, content={"detail": "Origin not allowed"})
        else:
            response = Response(status_code=204)
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            requested_headers = request.headers.get("access-control-request-headers", "")
            if requested_headers:
                response.headers["Access-Control-Allow-Headers"] = requested_headers
            response.headers["Access-Control-Max-Age"] = "600"
            response.headers["Vary"] = "Origin"
    else:
        response = await call_next(request)

    elapsed = max(0.0, time.perf_counter() - started)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        response.headers["Vary"] = "Origin"
    else:
        response.headers.pop("Access-Control-Allow-Origin", None)
    return response

@app.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        parts = values.split(",")
        if not parts or any(part.strip() == "" for part in parts):
            raise ValueError
        nums = [int(part.strip()) for part in parts]
    except (TypeError, ValueError):
        return JSONResponse(status_code=400, content={"detail": "values must be comma-separated integers"})
    total = sum(nums)
    return {"email": APP_EMAIL, "count": len(nums), "sum": total,
            "min": min(nums), "max": max(nums), "mean": total / len(nums)}

@app.get("/")
async def root():
    return {"status": "ok", "endpoint": "/stats?values=1,2,3"}

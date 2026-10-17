import time
import uuid

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

APP_EMAIL = "24f2000778@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-j3abmr.example.com"

app = FastAPI(title="CORS-Aware Metrics API")

# Handle CORS preflight requests through FastAPI's standard middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)


@app.middleware("http")
async def add_required_headers(request, call_next):
    start_time = time.perf_counter()
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    elapsed = max(0.0, time.perf_counter() - start_time)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"

    return response


@app.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        parts = values.split(",")
        if not parts or any(part.strip() == "" for part in parts):
            raise ValueError

        nums = [int(part.strip()) for part in parts]

    except (TypeError, ValueError):
        return JSONResponse(
            status_code=400,
            content={"detail": "values must be comma-separated integers"},
        )

    total = sum(nums)

    return {
        "email": APP_EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }


@app.get("/")
async def root():
    return {"status": "ok", "endpoint": "/stats?values=1,2,3"}

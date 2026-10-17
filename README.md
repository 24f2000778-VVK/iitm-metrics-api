# CORS-Aware Metrics API

Endpoint: `GET /stats?values=1,2,3`

## Deploy on Render
1. Put these files in a GitHub repository.
2. In Render, choose **New + -> Web Service** and connect that repository.
3. Use build command `pip install -r requirements.txt`.
4. Use start command `uvicorn app:app --host 0.0.0.0 --port $PORT`.
5. After deployment, submit the real `https://....onrender.com` service URL.

## Test
Visit `/stats?values=1,2,3`. Expected count 3, sum 6, min 1, max 3, mean 2.
Check every response has `X-Request-ID` and numeric `X-Process-Time`.

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "FastAPI Core is FUNCTIONAL on Vercel"}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, path: str):
    return JSONResponse({
        "received_path": path,
        "url_path": request.url.path,
        "method": request.method
    })

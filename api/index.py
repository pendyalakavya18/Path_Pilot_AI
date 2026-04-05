import os
import sys
import traceback

# 1. Setup paths
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 2. Environment override
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////tmp/pathpilot.db")
os.environ["CHROMA_PERSIST_DIR"] = os.getenv("CHROMA_PERSIST_DIR", "/tmp/chroma_db")
os.environ["UPLOAD_DIR"] = os.getenv("UPLOAD_DIR", "/tmp/uploads")

# 3. Create a wrapper app that EXPLICITLY handles the /api prefix
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    from main import app as backend_app
    
    app = FastAPI()

    @app.get("/api/health")
    async def health():
        return {"status": "ok", "message": "Vercel + FastAPI + Backend Integration is ALIVE"}

    # Mount the backend app under /api
    # This allows /api/auth/register to be routed to backend_app's /auth/register
    app.mount("/api", backend_app)

except Exception:
    import traceback
    from fastapi import FastAPI, Request
    from fastapi.responses import PlainTextResponse
    app = FastAPI()
    err = traceback.format_exc()
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def debug_error(request: Request):
        return PlainTextResponse(f"RE-INTEGRATION ERROR:\n{err}", status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

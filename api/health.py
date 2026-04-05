import os
import sys

# 1. Setup paths
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 2. Environment override
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////tmp/pathpilot.db")
os.environ["CHROMA_PERSIST_DIR"] = os.getenv("CHROMA_PERSIST_DIR", "/tmp/chroma_db")
os.environ["UPLOAD_DIR"] = os.getenv("UPLOAD_DIR", "/tmp/uploads")

# 3. Import backend application with fallback
try:
    from main import app
    from fastapi import Request
    from fastapi.responses import JSONResponse
    
    # Standard production root_path
    app.root_path = "/api"

    @app.get("/debug-info")
    async def debug_info(request: Request):
        return {
            "status": "ok",
            "source": "backend_app",
            "path": request.url.path,
            "root_path": request.scope.get("root_path")
        }

except Exception:
    import traceback
    from fastapi import FastAPI, Request
    from fastapi.responses import PlainTextResponse
    app = FastAPI()
    err = traceback.format_exc()
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def debug_error(request: Request):
        return PlainTextResponse(f"BACKEND IMPORT CRASH:\n{err}", status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

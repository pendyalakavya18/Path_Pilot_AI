import os
import sys

# 1. Setup paths without os.chdir
# Compute the path to the 'backend' directory
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
# Make absolute imports within backend/ work
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 2. Environment override for Vercel Read-Only FS
# We must set these BEFORE importing from main to ensure they are used during initialization
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////tmp/pathpilot.db")
os.environ["CHROMA_PERSIST_DIR"] = os.getenv("CHROMA_PERSIST_DIR", "/tmp/chroma_db")
os.environ["UPLOAD_DIR"] = os.getenv("UPLOAD_DIR", "/tmp/uploads")

# 3. Import backend application
try:
    from main import app
    # Set the root_path so FastAPI strips the /api prefix from Vercel requests
    app.root_path = "/api"
except Exception:
    # Fallback to diagnostic app if import fails
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

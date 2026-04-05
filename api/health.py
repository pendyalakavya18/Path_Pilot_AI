import os
import sys
import traceback

# 1. Setup paths
# Compute the path to the 'backend' directory
# index.py is at: c:\Desktop\PathPilotAI_Project\api\index.py
# backend is at: c:\Desktop\PathPilotAI_Project\backend\
current_dir = os.path.dirname(os.path.abspath(__file__)) # c:\Desktop\PathPilotAI_Project\api
root_dir = os.path.dirname(current_dir) # c:\Desktop\PathPilotAI_Project
backend_dir = os.path.join(root_dir, 'backend')

# Make absolute imports within backend/ work
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 2. Environment override for Vercel Read-Only FS
# We must set these BEFORE importing anything from backend to ensure they are used
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite+aiosqlite:////tmp/pathpilot.db")
os.environ["CHROMA_PERSIST_DIR"] = os.getenv("CHROMA_PERSIST_DIR", "/tmp/chroma_db")
os.environ["UPLOAD_DIR"] = os.getenv("UPLOAD_DIR", "/tmp/uploads")

# 3. Import backend application with fallback
try:
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    from main import app as backend_app
    from mangum import Mangum
    
    # Standard production root_path for Vercel
    backend_app.root_path = "/api"

    # Export the handler as 'app' for Vercel
    app = Mangum(backend_app, lifespan="off")

except Exception:
    # Diagnostic fallback app
    from fastapi import FastAPI, Request
    from fastapi.responses import PlainTextResponse
    app = FastAPI()
    err_msg = traceback.format_exc()
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def debug_error(request: Request):
        return PlainTextResponse(f"Vercel Startup Error:\n{err_msg}", status_code=500)

if __name__ == '__main__':
    import uvicorn
    # Vercel doesn't run this, but it's useful for local testing
    uvicorn.run(app, host='0.0.0.0', port=8000)

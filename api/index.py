import os
import sys
import traceback

# 1. IMMEDIATE ENV OVERRIDES for Vercel's Read-Only FS
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/pathpilot.db"
os.environ["CHROMA_PERSIST_DIR"] = "/tmp/chroma_db"
os.environ["UPLOAD_DIR"] = "/tmp/uploads"

# Ensure dirs exist
for d in ["/tmp/chroma_db", "/tmp/uploads"]:
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

# 2. PATH RESOLUTION
current_dir = os.path.dirname(os.path.abspath(__file__)) # c:\Desktop\PathPilotAI_Project\api
root_dir = os.path.dirname(current_dir) # c:\Desktop\PathPilotAI_Project
backend_dir = os.path.join(root_dir, 'backend')

# Make imports from both root and backend work
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# 3. MANGUM ASGI ADAPTER
try:
    from mangum import Mangum
    from backend.main import app as backend_app
    
    # Standard production root_path for Vercel
    backend_app.root_path = "/api"

    # Export the handler as 'app' for Vercel
    app = Mangum(backend_app, lifespan="off")

except Exception:
    from fastapi import FastAPI, Request
    from fastapi.responses import PlainTextResponse
    app = FastAPI()
    err_msg = traceback.format_exc()
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def debug_error(request: Request):
        return PlainTextResponse(f"Vercel Consolidation Error:\n{err_msg}", status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

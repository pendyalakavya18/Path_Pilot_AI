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

# 3. Create the handler using Mangum for reliable routing
try:
    from main import app
    from mangum import Mangum
    
    # We set root_path so routes match when Vercel hits /api
    app.root_path = "/api"
    
    # Export the handler as 'app' or 'handler' for Vercel
    handler = Mangum(app, lifespan="off")
    app = handler # Vercel also likes the name 'app'
    
except Exception:
    import traceback
    from fastapi import FastAPI
    from fastapi.responses import PlainTextResponse
    diagnostic_app = FastAPI()
    err = traceback.format_exc()
    @diagnostic_app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def debug_error(request):
        return PlainTextResponse(f"MANGUM WRAPPER ERROR:\n{err}", status_code=500)
    app = diagnostic_app

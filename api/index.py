import os
import sys

# Compute the path to the 'backend' directory
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')

# Make absolute imports within backend/ work
sys.path.insert(0, backend_dir)

# Set the working directory so relative paths resolve correctly
os.chdir(backend_dir)

# Ensure database is writable on Vercel's ephemeral filesystem if not configured
if not os.getenv("DATABASE_URL"):
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/pathpilot.db"
    
if not os.getenv("CHROMA_PERSIST_DIR"):
    os.environ["CHROMA_PERSIST_DIR"] = "/tmp/chroma_db"

if not os.getenv("UPLOAD_DIR"):
    os.environ["UPLOAD_DIR"] = "/tmp/uploads"

try:
    from main import app as main_app
    from fastapi import FastAPI
    import sys

    # Create a wrapper app to handle the /api prefix correctly in Vercel
    app = FastAPI()
    app.mount("/api", main_app)
except Exception as e:
    import traceback
    from fastapi import FastAPI, Request
    from fastapi.responses import PlainTextResponse
    
    app = FastAPI()
    err_msg = traceback.format_exc()
    
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    async def debug_error(request: Request):
        return PlainTextResponse(f"Vercel Startup Error:\n{err_msg}", status_code=500)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

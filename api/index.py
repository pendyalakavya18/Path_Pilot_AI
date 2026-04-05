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

from main import app

# Vercel needs standard execution layout
# Set root_path so FastAPI handles the /api prefix correctly in Vercel
app.root_path = "/api"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)

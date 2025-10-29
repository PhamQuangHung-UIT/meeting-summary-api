from fastapi import FastAPI

# Keep the application factory / app object here and include routers from submodules.
from app.auth import router as auth_router


app = FastAPI(title="Meeting Summary API")

# include auth endpoints
app.include_router(auth_router)


@app.get("/", summary="Health check")
def read_root():
    return {"status": "ok", "message": "Meeting Summary API"}

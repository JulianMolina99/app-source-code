from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.api.endpoints import router

app = FastAPI()

# Custom error handler for 404 errors
@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    """Handles 404 errors for undefined routes."""
    return JSONResponse(status_code=404, content={"message": "ERROR"})

# Custom error handler for 405 Method Not Allowed errors
@app.exception_handler(405)
async def custom_405_handler(request: Request, exc):
    """Handles 405 errors for disallowed HTTP methods."""
    return JSONResponse(status_code=405, content={"message": "ERROR"})

# Include routes from the router
app.include_router(router)

# Restrict access to non /DevOps endpoints
@app.middleware("http")
async def restrict_other_paths(request: Request, call_next):
    """Middleware that returns a 404 error if the path does not start with /DevOps."""
    path = request.url.path
    if not path.startswith("/DevOps"):
        return JSONResponse(status_code=404, content={"message": "ERROR"})

    # Call the next layer if the path is valid
    response = await call_next(request)
    return response

# Entry point for running Uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
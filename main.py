"""
Main FastAPI Application
CarbonCALC: Real-Time Carbon Footprint Monitoring and Predictive Reporting Cloud Solution
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from database.database import init_db
from api.routes import router
import os

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="CarbonCALC",
    description="Real-Time Carbon Footprint Monitoring and Predictive Reporting Cloud Solution",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount dashboard files
if os.path.exists("dashboard"):
    app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard"""
    try:
        with open("dashboard/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="""
            <!DOCTYPE html>
            <html>
            <head><title>CarbonCALC</title></head>
            <body>
                <h1>CarbonCALC - Carbon Footprint Monitoring System</h1>
                <p>Dashboard is being set up. Please check back soon.</p>
            </body>
            </html>
            """,
            status_code=200
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "CarbonCALC"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


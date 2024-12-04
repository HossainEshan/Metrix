from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.api.routers.endpoints import endpoints_router

app: FastAPI = FastAPI()


def get_http_client():
    return app.state.http_client


app.include_router(endpoints_router)

templates = Jinja2Templates(directory="src/static/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


# Route to serve the admin dashboard
@app.get("/dashboard")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/status")
def health_check():
    return {"status": "Running"}

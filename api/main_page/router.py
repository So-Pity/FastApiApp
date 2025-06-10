from fastapi import APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from modules.dependencies import session_depend

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
templates_path = os.path.join(BASE_DIR, "templates")
static_path = os.path.join(BASE_DIR, "static")

router.mount("/static", StaticFiles(directory=static_path, html=True), name="static")
templates = Jinja2Templates(directory=templates_path)

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def show_main_page(request: Request):
  base_url = request.url
  link_to_swagger = f"{base_url}docs"
  link_to_redoc = f"{base_url}redoc"

  return templates.TemplateResponse(
    "home.html",
    {
      "request": request,
      "swagger": link_to_swagger,
      "redoc": link_to_redoc,
    }
  )
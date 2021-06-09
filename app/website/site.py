from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.requests import Request

router = APIRouter()

# These paths seem fragile
templates = Jinja2Templates(directory="./website/templates")

@router.get("/")
@router.get("/index.html")
async def login(request: Request):
    return templates.TemplateResponse("./index.html", context={'request': request})


@router.get("/signup")
@router.get("/signup.html")
async def signup(request: Request):
    return templates.TemplateResponse("./signup.html", context={'request': request})

@router.get("/home")
@router.get("/home.html")
async def home(request: Request):
    return templates.TemplateResponse("./home.html", context={'request': request})
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import item_master

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request
        }
    )
    
@app.get("/{category}")
def breakfast(request: Request, category: str):
    items = list(item_master.find({"category": category}))
    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "items": items, 
       }
    )
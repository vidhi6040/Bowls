from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import item_master, user_master

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
    
@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html", 
        {
            "request": request
        }
    )
    
@app.post("/register")
def register(name: str = Form(...), email: str = Form(...), password: str = Form(...)):
        existing_user = users.find_one({"email": email})
        if existing_user:
            return {'message': "User already exists"}

    
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html", 
        {
            "request": request
        }
    )
    

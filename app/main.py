from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import item_master, user_master
from starlette.middleware.sessions import SessionMiddleware
from bson import ObjectId

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

@app.get("/")
def home(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse(
        "home.html", 
        {
            "request": request,
            'user': user
        }
    )
    
@app.get("/register")
def register_page(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "user": user
        }
    )
    
@app.post("/register")
def register(request: Request, name: str=Form(...), password: str=Form(...), email: str=Form(...)):
    if not name or not email or not password:
        return {"message": "All fields are mandatory."}
    user = user_master.find_one({"email": email})
    if user:
        return {'message': 'User already exists. Please log in.'}
    user_master.insert_one({
        "name": name,
        "email": email,
        "password": password
    })
    return RedirectResponse('/login', status_code=303)

@app.get("/login")
def login_page(request: Request):
    user = request.session.get("user")
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            'user': user
        }
    )
    
@app.post("/login")
def login(request: Request, email: str=Form(...), password: str=Form(...)):
    if not email or not password:
        return {"message": "All fields are mandatory."}
    user = user_master.find_one({"email": email, "password": password})
    if not user:
        return {'message': 'User not found. Please register first.'}   
    if user:
        request.session['user'] = {
            "name": user["name"],
            "email": user["email"]
        } 
    return RedirectResponse('/', status_code=303)        

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

@app.get("/{category}")
def menu(request: Request, category: str):
    items = list(item_master.find({"category": category}))
    user = request.session.get('user')
    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "items": items, 
            "user": user
       }
    )
    
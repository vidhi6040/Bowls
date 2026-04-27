from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.database import item_master, user_master, cart_master
from starlette.middleware.sessions import SessionMiddleware
from bson import ObjectId

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# Home
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
    
# Register
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
    existing = user_master.find_one({"email": email})
    if existing:
        return {'message': 'User already exists. Please log in.'}
    user_master.insert_one({
        "name": name,
        "email": email,
        "password": password
    })
    return RedirectResponse('/login', status_code=303)

# Login
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
    existing = user_master.find_one({"email": email, "password": password})
    if not existing:
        return {'message': 'User not found. Please register first.'}   
    else:
        request.session['user'] = {
            "name": existing["name"],
            "email": existing["email"]
        } 
    return RedirectResponse('/', status_code=303)        

# Logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)

# Menu
@app.get("/{category}")
def menu(request: Request, category: str):
    items = list(item_master.find({"category": category}))
    user = request.session.get('user')
    if user:
        cart_items = list(cart_master.find({"email": user["email"]}))
        cart_map = {item["item_code"]: item["quantity"] for item in cart_items}

        for item in items:
            item["quantity"] = cart_map.get(item["item_code"], 0)
    else:
        for item in items:
            item["quantity"] = 0
    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "items": items, 
            "user": user
       }
    )
    
# Cart
@app.post("/add_to_cart")
def cart(request: Request, item_code: str=Form(...), name: str=Form(...), price: float=Form(...), quantity: int=Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse('/login', status_code=303)
    existing = cart_master.find_one({"email": user["email"], "item_code": item_code})
    total = price * quantity
    if existing:
        cart_master.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": 1, "total": price}}
        )
    else:
        cart_master.insert_one({
            "email": user["email"],
            "item_code": item_code,
            "name": name,
            "price": price,
            "quantity": quantity,
            "total": total
        })
    return RedirectResponse(request.headers.get("referer"), status_code=303)

@app.post("/update_cart")
def update_cart(request: Request, item_code: str=Form(...), action: str=Form(...)):
    user = request.session.get("user")
    existing = cart_master.find_one({
        "email": user["email"],
        "item_code": item_code
    })
    if not user:
        return RedirectResponse("/login", status_code=303)
    if not existing:
        return RedirectResponse("/", status_code=303)
    if action == "increase":
        cart_master.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": 1, "total": existing["price"]}}
        )
    elif action == "decrease":
        if existing["quantity"] > 1:
            cart_master.update_one(
                {"_id": existing["_id"]},
                {"$inc": {"quantity": -1, "total": -existing["price"]}}
            )
        else:
            cart_master.delete_one({"_id": existing["_id"]})
    return RedirectResponse(request.headers.get("referer"), status_code=303)
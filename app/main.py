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
    existing_user = user_master.find_one({"email": email})
    if existing_user:
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
    existing_user = user_master.find_one({"email": email, "password": password})
    if not existing_user:
        return {'message': 'User not found. Please register first.'}   
    else:
        request.session['user'] = {
            "name": existing_user["name"],
            "email": existing_user["email"]
        } 
    return RedirectResponse('/', status_code=303)        

# Logout
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)
    
# Cart
@app.post("/add_to_cart")
def add_to_cart(request: Request, item_code: str=Form(...), name: str=Form(...), price: float=Form(...), quantity: int=Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse('/login', status_code=303)
    existing_cart = cart_master.find_one({"email": user["email"], "item_code": item_code})
    total = price * quantity
    if existing_cart:
        cart_master.update_one(
            {"_id": existing_cart["_id"]},
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
    return RedirectResponse("/cart", status_code=303)

@app.post("/update_cart")
def update_cart(request: Request, item_code: str=Form(...), action: str=Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    existing_cart = cart_master.find_one({
        "email": user["email"],
        "item_code": item_code
    })
    if not existing_cart:
        return RedirectResponse("/cart", status_code=303)
    if action == "increase":
        cart_master.update_one(
            {"_id": existing_cart["_id"]},
            {"$inc": {"quantity": 1, "total": existing_cart["price"]}}
        )
    elif action == "decrease":
        if existing_cart["quantity"] > 1:
            cart_master.update_one(
                {"_id": existing_cart["_id"]},
                {"$inc": {"quantity": -1, "total": -existing_cart["price"]}}
            )
        else:
            cart_master.delete_one({"_id": existing_cart["_id"]})
    return RedirectResponse("/cart", status_code=303)

@app.get("/cart")
def cart(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    cart_items = list(cart_master.find({"email": user["email"]}))
    final_amount = sum(item["total"] for item in cart_items)
    return templates.TemplateResponse(
        "cart.html",
        {
            "request": request,
            "items": cart_items,
            "user": user,
            "final_amount": final_amount
        }
    )
    
#Profile
@app.get("/profile")
def profile(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse('/login', status_code=303)
    
    items = list(cart_master.find({"email": user["email"]}))
    total_items = sum(item["quantity"] for item in items)
    total_amount =  sum(item["total"] for item in items)
    
    orders = []
    
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": user,
            "total_items": total_items,
            "total_amount": total_amount,
            "orders": orders
        }
    )

@app.post("/change_password")
def change_password(request: Request, old_password: str=Form(...), new_password: str=Form(...), confirm_password: str=Form(...)):
    user = request.session.get("user")
    if not user:
        return RedirectResponse("/login", status_code=303)
    existing_user = user_master.find_one({"email": user["email"]})
    if existing_user["password"] != old_password:
        return {"message": "Old password is incorrect"}
    if new_password != confirm_password:
        return {"message": "Passwords do not match"}
    user_master.update_one(
        {'email': existing_user['email']}, 
        {"$set": {'password': new_password}}
    )
    return RedirectResponse('/profile', status_code=303)
        
# Menu
@app.get("/{category}")
def menu(request: Request, category: str):
    menu_items = list(item_master.find({"category": category}))
    user = request.session.get('user')
    if user:
        cart_items = list(cart_master.find({"email": user["email"]}))
        cart_map = {item["item_code"]: item["quantity"] for item in cart_items}

        for item in menu_items:
            item["quantity"] = cart_map.get(item["item_code"], 0)
    else:
        for item in menu_items:
            item["quantity"] = 0       
    menu_title = category.capitalize()
    return templates.TemplateResponse(
        "menu.html",
        {
            "request": request,
            "items": menu_items, 
            "user": user,
            "menu_title": menu_title
       }
    )
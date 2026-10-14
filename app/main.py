from datetime import datetime
from pathlib import Path
import os

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from passlib.context import CryptContext

from app.database import item_master, user_master, cart_master


# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

app = FastAPI()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Development default only.
# Set BOWLS_SESSION_SECRET before deployment.
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv(
        "BOWLS_SESSION_SECRET",
        "change-this-secret-before-deployment"
    )
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"user": request.session.get("user")}
    )


# --------------------------------------------------
# CUSTOMER REGISTRATION
# --------------------------------------------------

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "user": request.session.get("user"),
            "error": None
        }
    )


@app.post("/register")
def register(
    request: Request,
    name: str = Form(...),
    password: str = Form(...),
    email: str = Form(...)
):
    name = name.strip()
    email = email.strip().lower()

    if not name or not email or not password:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "user": None,
                "error": "All fields are mandatory."
            },
            status_code=400
        )

    if user_master.find_one({"email": email}):
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "user": None,
                "error": "User already exists. Please log in."
            },
            status_code=400
        )

    user_master.insert_one({
        "name": name,
        "email": email,
        # Hash passwords before public deployment.
        "password": password,
        "role": "user",
        "created_at": datetime.now()
    })

    return RedirectResponse("/login", status_code=303)


# --------------------------------------------------
# CUSTOMER LOGIN
# Admin login and admin routes are disabled for now.
# --------------------------------------------------

@app.get("/login")
def login_page(request: Request):
    if request.session.get("user"):
        return RedirectResponse("/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "user": None,
            "error": None
        }
    )


@app.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    email = email.strip().lower()

    existing_user = user_master.find_one({
        "email": email,
        "password": password
    })

    if (
        not existing_user
        or existing_user.get("role", "user") == "admin"
    ):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={
                "user": None,
                "error": "Invalid email or password."
            },
            status_code=400
        )

    request.session.clear()
    request.session["user"] = {
        "name": existing_user.get("name", ""),
        "email": existing_user["email"]
    }

    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# CUSTOMER LOGOUT
# --------------------------------------------------

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


# --------------------------------------------------
# ADD ITEM TO CART
# --------------------------------------------------

@app.post("/add_to_cart")
def add_to_cart(
    request: Request,
    item_code: str = Form(...),
    name: str = Form(""),
    price: float = Form(0),
    quantity: int = Form(...)
):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    if quantity < 1:
        return RedirectResponse("/", status_code=303)

    product = item_master.find_one({"item_code": item_code})

    if not product or product.get("available", True) is False:
        return RedirectResponse("/", status_code=303)

    # Use the price stored in MongoDB.
    actual_price = float(product["price"])
    email = user["email"]

    existing_cart = cart_master.find_one({
        "email": email,
        "item_code": item_code
    })

    if existing_cart:
        cart_master.update_one(
            {"_id": existing_cart["_id"]},
            {
                "$inc": {
                    "quantity": quantity,
                    "total": actual_price * quantity
                },
                "$set": {
                    "name": product["name"],
                    "price": actual_price
                }
            }
        )
    else:
        cart_master.insert_one({
            "email": email,
            "item_code": item_code,
            "name": product["name"],
            "price": actual_price,
            "quantity": quantity,
            "total": actual_price * quantity
        })

    return RedirectResponse("/cart", status_code=303)


# --------------------------------------------------
# UPDATE CART QUANTITY
# --------------------------------------------------

@app.post("/update_cart")
def update_cart(
    request: Request,
    item_code: str = Form(...),
    action: str = Form(...)
):
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
            {
                "$inc": {
                    "quantity": 1,
                    "total": float(existing_cart["price"])
                }
            }
        )

    elif action == "decrease":
        if existing_cart.get("quantity", 1) > 1:
            cart_master.update_one(
                {"_id": existing_cart["_id"]},
                {
                    "$inc": {
                        "quantity": -1,
                        "total": -float(existing_cart["price"])
                    }
                }
            )
        else:
            cart_master.delete_one({
                "_id": existing_cart["_id"]
            })

    return RedirectResponse("/cart", status_code=303)


# --------------------------------------------------
# CUSTOMER CART
# --------------------------------------------------

@app.get("/cart")
def cart(request: Request):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    cart_items = list(
        cart_master.find({"email": user["email"]})
    )

    final_amount = sum(
        float(item.get("total", 0))
        for item in cart_items
    )

    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "items": cart_items,
            "user": user,
            "final_amount": final_amount
        }
    )


# --------------------------------------------------
# CUSTOMER PROFILE
# --------------------------------------------------

@app.get("/profile")
def profile(request: Request):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    cart_items = list(
        cart_master.find({"email": user["email"]})
    )

    total_items = sum(
        item.get("quantity", 0)
        for item in cart_items
    )

    total_amount = sum(
        float(item.get("total", 0))
        for item in cart_items
    )

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user,
            "total_items": total_items,
            "total_amount": total_amount,
            "orders": [],
            "error": None
        }
    )


# --------------------------------------------------
# CHANGE PASSWORD
# --------------------------------------------------

@app.post("/change_password")
def change_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    user = request.session.get("user")

    if not user:
        return RedirectResponse("/login", status_code=303)

    existing_user = user_master.find_one({
        "email": user["email"]
    })

    if not existing_user:
        request.session.clear()
        return RedirectResponse("/login", status_code=303)

    cart_items = list(
        cart_master.find({"email": user["email"]})
    )

    total_items = sum(
        item.get("quantity", 0)
        for item in cart_items
    )

    total_amount = sum(
        float(item.get("total", 0))
        for item in cart_items
    )

    error = None

    if existing_user.get("password") != old_password:
        error = "Old password is incorrect."
    elif not new_password:
        error = "New password cannot be empty."
    elif new_password != confirm_password:
        error = "New passwords do not match."

    if error:
        return templates.TemplateResponse(
            request=request,
            name="profile.html",
            context={
                "user": user,
                "total_items": total_items,
                "total_amount": total_amount,
                "orders": [],
                "error": error
            },
            status_code=400
        )

    user_master.update_one(
        {"email": user["email"]},
        {"$set": {"password": new_password}}
    )

    return RedirectResponse("/profile", status_code=303)


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

@app.get("/about")
def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={"user": request.session.get("user")}
    )


# --------------------------------------------------
# CONTACT PAGE
# --------------------------------------------------

@app.get("/contact")
def contact(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="contact.html",
        context={"user": request.session.get("user")}
    )


# --------------------------------------------------
# CUSTOMER MENU
# Keep this catch-all route LAST.
# --------------------------------------------------

@app.get("/{category}")
def menu(request: Request, category: str):
    allowed_categories = {
        "breakfast",
        "lunch",
        "dinner"
    }

    if category not in allowed_categories:
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={"user": request.session.get("user")}
        )

    menu_items = list(
        item_master.find({
            "category": category,
            "available": {"$ne": False}
        })
    )

    user = request.session.get("user")
    cart_map = {}

    if user:
        cart_items = list(
            cart_master.find({"email": user["email"]})
        )

        cart_map = {
            item["item_code"]: item.get("quantity", 0)
            for item in cart_items
        }

    for item in menu_items:
        item["quantity"] = cart_map.get(
            item["item_code"], 0
        )

    return templates.TemplateResponse(
        request=request,
        name="menu.html",
        context={
            "items": menu_items,
            "user": user,
            "menu_title": category.capitalize()
        }
    )

import os
from decimal import Decimal
from flask import Flask, abort, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "local-development-key-change-me")

PRODUCTS = {
    "p101": {"name": "Everyday Backpack", "category": "Accessories", "price": Decimal("1299.00"), "emoji": "🎒", "description": "A lightweight backpack for work, study, and weekends."},
    "p102": {"name": "Wireless Headphones", "category": "Electronics", "price": Decimal("2499.00"), "emoji": "🎧", "description": "Comfortable over-ear sound for your daily commute."},
    "p103": {"name": "Classic Watch", "category": "Accessories", "price": Decimal("1899.00"), "emoji": "⌚", "description": "A clean, everyday design with a soft strap."},
    "p104": {"name": "Running Sneakers", "category": "Footwear", "price": Decimal("3299.00"), "emoji": "👟", "description": "Cushioned comfort for walks, runs, and busy days."},
}

def cart_details():
    cart = session.get("cart", {})
    lines = []
    subtotal = Decimal("0.00")
    for product_id, quantity in cart.items():
        product = PRODUCTS.get(product_id)
        if product and isinstance(quantity, int) and quantity > 0:
            line_total = product["price"] * quantity
            lines.append({
                "id": product_id,
                "name": product["name"],
                "price": product["price"],
                "emoji": product["emoji"],
                "quantity": quantity,
                "line_total": line_total,
            })
            subtotal += line_total
    return lines, subtotal

@app.get("/")
def home():
    _, _ = cart_details()
    cart_count = sum(session.get("cart", {}).values())
    return render_template("index.html", products=PRODUCTS, cart_count=cart_count)

@app.post("/cart/add/<product_id>")
def add_to_cart(product_id):
    if product_id not in PRODUCTS:
        abort(404)
    cart = session.get("cart", {})
    cart[product_id] = min(int(cart.get(product_id, 0)) + 1, 99)
    session["cart"] = cart
    return redirect(url_for("home"))

@app.get("/cart")
def view_cart():
    lines, subtotal = cart_details()
    cart_count = sum(item["quantity"] for item in lines)
    return render_template("cart.html", lines=lines, subtotal=subtotal, cart_count=cart_count)

@app.post("/cart/update/<product_id>")
def update_cart(product_id):
    if product_id not in PRODUCTS:
        abort(404)
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 1
    cart = session.get("cart", {})
    if quantity <= 0:
        cart.pop(product_id, None)
    else:
        cart[product_id] = min(quantity, 99)
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.post("/cart/remove/<product_id>")
def remove_from_cart(product_id):
    cart = session.get("cart", {})
    cart.pop(product_id, None)
    session["cart"] = cart
    return redirect(url_for("view_cart"))

@app.post("/cart/clear")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("view_cart"))

@app.get("/checkout")
def checkout():
    lines, subtotal = cart_details()
    shipping = Decimal("0.00") if subtotal == 0 or subtotal >= Decimal("3000.00") else Decimal("99.00")
    total = subtotal + shipping
    cart_count = sum(item["quantity"] for item in lines)
    return render_template("checkout.html", lines=lines, subtotal=subtotal,
                           shipping=shipping, total=total, cart_count=cart_count)

if __name__ == "__main__":
    app.run(debug=True)

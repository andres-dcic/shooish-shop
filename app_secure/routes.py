from flask import Blueprint, request, session, redirect, url_for, render_template_string, abort
from markupsafe import escape
import sqlite3
from .db import connect

bp = Blueprint("shop", __name__)

BASE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Shooish Shop - SECURE</title>
<style>
:root { --primary: #0d47a1; --success: #1b5e20; --info: #0277bd; }
body { font-family: Arial, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f5f7fa; }
.secure-badge { background: var(--primary); color: white; padding: 8px 12px; border-radius: 4px; font-size: 12px; font-weight: bold; display: inline-block; margin-bottom: 20px; }
nav { margin-bottom: 30px; padding: 15px 0; padding-bottom: 15px; border-bottom: 3px solid var(--primary); }
nav a { margin-right: 18px; color: var(--primary); text-decoration: none; font-weight: 500; }
nav a:hover { text-decoration: underline; }
.card { border: 2px solid var(--primary); border-radius: 8px; padding: 16px; margin: 12px 0; background: white; }
h1, h2 { color: var(--primary); }
input, button { padding: 9px; margin: 4px; border-radius: 4px; border: 1px solid #ccc; }
button { cursor: pointer; background: var(--success); color: white; border: none; font-weight: bold; transition: background 0.2s; }
button:hover { background: #0d3b1a; }
.warn { background: #e3f2fd; padding: 12px; border-radius: 6px; border-left: 4px solid var(--info); color: #01579b; }
.ok { background: #e8f5e9; padding: 12px; border-radius: 6px; border-left: 4px solid var(--success); color: #1b5e20; }
</style>
</head>
<body>
<div class="secure-badge">🔒 SECURE VERSION</div>
<nav>
<a href="/">Shop</a>
<a href="/search">Search</a>
<a href="/orders">My orders</a>
<a href="/profile">Profile</a>
{% if session.get("user_id") %}
<a href="/logout">Logout</a>
{% else %}
<a href="/login">Login</a>
{% endif %}
</nav>
__CONTENT__
</body>
</html>"""

def page(content, **context):
    return render_template_string(BASE.replace("__CONTENT__", content), **context)

@bp.route("/")
def index():
    con = connect()
    products = con.execute("SELECT * FROM products ORDER BY id").fetchall()
    con.close()
    return page("""
    <h1>Shooish Shop</h1>
    <p>Simple online shop used for the security workshop.</p>
    {% for p in products %}
      <div class="card">
        <h2>{{ p["name"] }}</h2>
        <p>{{ p["description"] }}</p>
        <strong>${{ "%.2f"|format(p["price"]) }}</strong>
        <form method="post" action="/buy/{{ p['id'] }}">
          <button type="submit">Buy</button>
        </form>
      </div>
    {% endfor %}
    """, products=products)

@bp.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        con = connect()

        # FIX: Use parameterized query to prevent SQL injection
        try:
            user = con.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()
        except sqlite3.Error as exc:
            user = None
            message = f"Database error: {exc}"

        con.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("shop.index"))

        message = message or "Invalid credentials"

    return page(f"""
    <h1>Login</h1>
    <p class="warn">Training application. Credentials are demo-only.</p>
    <p>{message}</p>
    <form method="post">
      <input name="username" placeholder="Username" autocomplete="username">
      <input name="password" placeholder="Password" type="password" autocomplete="current-password">
      <button type="submit">Login</button>
    </form>
    """)

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("shop.index"))

@bp.route("/buy/<int:product_id>", methods=["POST"])
def buy(product_id):
    if not session.get("user_id"):
        return redirect(url_for("shop.login"))

    con = connect()
    product = con.execute("SELECT id FROM products WHERE id = ?", (product_id,)).fetchone()
    if not product:
        con.close()
        abort(404)

    con.execute(
        "INSERT INTO orders(user_id, product_id, quantity, status) VALUES (?, ?, ?, ?)",
        (session["user_id"], product_id, 1, "paid")
    )
    con.commit()
    con.close()
    return redirect(url_for("shop.orders"))

@bp.route("/orders")
def orders():
    if not session.get("user_id"):
        return redirect(url_for("shop.login"))

    con = connect()
    rows = con.execute("""
        SELECT o.id, o.status, o.quantity, p.name, p.price
        FROM orders o
        JOIN products p ON p.id = o.product_id
        WHERE o.user_id = ?
        ORDER BY o.id
    """, (session["user_id"],)).fetchall()
    con.close()

    return page("""
    <h1>My orders</h1>
    {% for o in rows %}
      <div class="card">
        <strong>Order #{{ o["id"] }}</strong><br>
        Product: {{ o["name"] }}<br>
        Quantity: {{ o["quantity"] }}<br>
        Status: {{ o["status"] }}<br>
        <a href="/order?id={{ o['id'] }}">View order</a>
      </div>
    {% else %}
      <p>No orders.</p>
    {% endfor %}
    """, rows=rows)

@bp.route("/order")
def order_detail():
    if not session.get("user_id"):
        return redirect(url_for("shop.login"))

    order_id = request.args.get("id", "")

    con = connect()

    # FIX: Validate that the order belongs to the logged-in user (prevent IDOR/BOLA)
    order = con.execute("""
        SELECT o.id, o.status, o.quantity, p.name, p.price, u.username
        FROM orders o
        JOIN products p ON p.id = o.product_id
        JOIN users u ON u.id = o.user_id
        WHERE o.id = ? AND o.user_id = ?
    """, (order_id, session["user_id"])).fetchone()

    con.close()

    if not order:
        abort(404)

    return page(f"""
    <h1>Order #{order["id"]}</h1>
    <div class="card">
      <strong>Customer:</strong> {order["username"]}<br>
      <strong>Product:</strong> {order["name"]}<br>
      <strong>Quantity:</strong> {order["quantity"]}<br>
      <strong>Status:</strong> {order["status"]}<br>
      <strong>Price:</strong> ${order["price"]}
    </div>
    """)

@bp.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("shop.login"))

    con = connect()
    user = con.execute(
        "SELECT id, username, role FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()
    con.close()

    return page(f"""
    <h1>Profile</h1>
    <div class="card">
      Username: {user["username"]}<br>
      Role: {user["role"]}
    </div>
    """)

@bp.route("/search")
def search():
    term = request.args.get("q", "").strip()
    results = []

    # FIX: Actual search functionality + parameterized query
    if term:
        con = connect()
        results = con.execute(
            "SELECT id, name, description, price FROM products WHERE name LIKE ? OR description LIKE ?",
            (f"%{term}%", f"%{term}%")
        ).fetchall()
        con.close()

    # FIX: Escape untrusted input to prevent XSS
    safe_term = escape(term)

    return page(f"""
    <h1>Search</h1>
    <p>Results for: <strong>{safe_term}</strong></p>
    <form method="get">
      <input name="q" value="{safe_term}" placeholder="Search products">
      <button type="submit">Search</button>
    </form>
    {f'<div style="margin-top: 20px;">' if results else ''}
    {''.join([f'''
      <div class="card">
        <h3>{escape(r["name"])}</h3>
        <p>{escape(r["description"])}</p>
        <strong>${"%.2f"|format(r["price"])}</strong>
        <form method="post" action="/buy/{r["id"]}">
          <button type="submit">Buy</button>
        </form>
      </div>
    ''' for r in results])}
    {f'</div>' if results else '<p>No products found.</p>' if term else ''}
    """)

@bp.route("/health")
def health():
    return {"status": "ok"}

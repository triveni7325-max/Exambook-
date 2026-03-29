from flask import Flask, session, redirect, request
import os

app = Flask(__name__)

# 🔐 SECRET KEY (fixed)
app.secret_key = "secret123"


# =========================
# 🔐 ADMIN AUTH
# =========================
from register import register_bp
from login import login_bp

# =========================
# 🛠️ ADMIN PANEL
# =========================
from users import users_bp
from category import category_bp
from quiz import quiz_bp
from question import question_bp
from bulk_question import bulk_bp

# =========================
# 🌍 USER SIDE
# =========================
from auth import auth_bp
from home import home_bp
from quiz import user_quiz_bp
from play import play_bp
from score import score_bp


# =========================
# 🔗 REGISTER BLUEPRINTS
# =========================

# ADMIN
app.register_blueprint(users_bp, url_prefix="/admin")
app.register_blueprint(register_bp, url_prefix="/admin")
app.register_blueprint(login_bp, url_prefix="/admin")

app.register_blueprint(category_bp, url_prefix="/admin")
app.register_blueprint(quiz_bp, url_prefix="/admin")
app.register_blueprint(question_bp, url_prefix="/admin")
app.register_blueprint(bulk_bp, url_prefix="/admin")

# USER
app.register_blueprint(auth_bp)              # /login /register
app.register_blueprint(home_bp)              # /
app.register_blueprint(user_quiz_bp, url_prefix="/user")
app.register_blueprint(play_bp, url_prefix="/user")
app.register_blueprint(score_bp, url_prefix="/user")   # ✅ FIX


# =========================
# 🔒 LOGIN PROTECTION
# =========================
@app.before_request
def protect():

    open_routes = ["/login", "/register", "/admin/login", "/admin/register", "/static"]

    # 👉 Admin + User दोनों check
    if not any(request.path.startswith(route) for route in open_routes):

        if request.path.startswith("/admin"):
            if "admin_id" not in session:
                return redirect("/admin/login")
        else:
            if "user_id" not in session:
                return redirect("/login")


# =========================
# 🚀 RUN
# =========================
if __name__ == "__main__":
    app.run(debug=True)

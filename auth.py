from flask import Blueprint, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        try:
            cur.execute("""
            INSERT INTO users (name,email,mobile,password)
            VALUES (?,?,?,?)
            """, (name,email,mobile,hashed))

            conn.commit()
            conn.close()

            return redirect("/login")

        except:
            conn.close()
            return "Mobile already exists!"

    return render_template("user/register.html")


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        mobile = request.form["mobile"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE mobile=?", (mobile,))
        user = cur.fetchone()

        conn.close()

        if user and check_password_hash(user[4], password):

            session["user_id"] = user[0]
            session["user_name"] = user[1]

            # 🔥 CHANGE HERE
            return render_template("user/login_success.html")

        else:
            return "Invalid Mobile or Password"

    return render_template("user/login.html")


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
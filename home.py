from flask import Blueprint, render_template
import sqlite3

home_bp = Blueprint(
    "home",
    __name__,
    template_folder="../../templates/user"
)

@home_bp.route("/")
def home():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # only published category
    cur.execute("""
SELECT id, name FROM categories
WHERE id IN (
    SELECT category_id FROM published_categories
)
""")
    categories = cur.fetchall()

    conn.close()

    return render_template("home.html", categories=categories)
from flask import Blueprint, render_template, session
import sqlite3

score_bp = Blueprint("score", __name__)

@score_bp.route("/user/score")
def score():

    user_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # latest result
    cur.execute("""
    SELECT score, right_ans, wrong_ans, skipped, created_at
    FROM results
    WHERE user_id=?
    ORDER BY id DESC LIMIT 1
    """, (user_id,))

    result = cur.fetchone()
    conn.close()

    return render_template("user/score.html", result=result)
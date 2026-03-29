from flask import Blueprint, render_template, session, redirect
import sqlite3

user_quiz_bp = Blueprint(
    "user_quiz",
    __name__,
    template_folder="../../templates/user"
)

@user_quiz_bp.route("/user_quiz/<int:category_id>")
def user_quiz(category_id):

    # 🔐 login check
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # ✅ सभी published quizzes
    cur.execute("""
    SELECT id, quiz_name FROM quizzes
    WHERE category_id=?
    AND id IN (SELECT quiz_id FROM published_quizzes)
    """, (category_id,))

    quizzes = cur.fetchall()

    final_data = []

    # 🔥 हर quiz के लिए check करो attempt हुआ या नहीं
    for q in quizzes:
        quiz_id = q[0]

        cur.execute("""
        SELECT id FROM results
        WHERE user_id=? AND quiz_id=?
        """, (user_id, quiz_id))

        attempted = cur.fetchone()

        final_data.append({
            "id": quiz_id,
            "name": q[1],
            "attempted": True if attempted else False
        })

    conn.close()

    return render_template("quiz.html", quizzes=final_data)
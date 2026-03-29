from flask import Blueprint, render_template, request, session, redirect
import sqlite3

play_bp = Blueprint("play", __name__)

@play_bp.route("/play/<int:quiz_id>", methods=["GET","POST"])
def play(quiz_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # all questions
    cur.execute("""
    SELECT id, question, option1, option2, option3, option4, correct
    FROM questions WHERE quiz_id=?
    """, (quiz_id,))
    
    questions = cur.fetchall()

    # ✅ TIMER
    cur.execute("SELECT time FROM quizzes WHERE id=?", (quiz_id,))
    quiz_time = cur.fetchone()[0]

    # =========================
    # 👉 SUBMIT
    # =========================
    if request.method == "POST":

        # 🔐 user check
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login")

        result = []

        right = 0
        wrong = 0
        skipped = 0
        score = 0

        for q in questions:
            qid = q[0]

            data = {
                "question": q[1],
                "A": q[2],
                "B": q[3],
                "C": q[4],
                "D": q[5],
                "correct": q[6]
            }

            # ⚠️ IMPORTANT (same name use होना चाहिए HTML में)
            user_ans = request.form.get(f"q{qid}")

            if user_ans is None:
                skipped += 1
            elif user_ans == q[6]:
                right += 1
                score += 2
            else:
                wrong += 1
                score -= 4

            data["user"] = user_ans
            result.append(data)

        # =========================
        # ✅ SAVE RESULT IN DB
        # =========================
        cur.execute("""
        INSERT INTO results (user_id, quiz_id, score, right_ans, wrong_ans, skipped)
        VALUES (?,?,?,?,?,?)
        """, (user_id, quiz_id, score, right, wrong, skipped))

        conn.commit()
        conn.close()

        # 👉 result page
        return render_template(
            "user/result.html",
            result=result,
            right=right,
            wrong=wrong,
            skipped=skipped,
            score=score
        )

    conn.close()

    return render_template(
        "user/play.html",
        questions=questions,
        quiz_time=quiz_time
    )
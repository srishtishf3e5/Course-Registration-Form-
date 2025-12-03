import os
from flask import (
    Flask, render_template, request,
    redirect, url_for, session, flash
)
from db import get_db, close_db, init_db, DB_PATH

app = Flask(__name__)
app.secret_key = "change_this_secret_key"  # for session


@app.teardown_appcontext
def teardown_db(exception):
    close_db()


def ensure_database():
    # Create DB and tables on first run
    if not os.path.exists(DB_PATH):
        with app.app_context():
            init_db()
            print("Database initialized.")


def get_current_user():
    if "user_id" in session:
        return {
            "id": session["user_id"],
            "name": session["user_name"],
            "email": session["user_email"],
        }
    return None


@app.route("/")
def index():
    user = get_current_user()
    return render_template("index.html", user=user)


@app.route("/register", methods=["GET", "POST"])
def register():
    user = get_current_user()
    if request.method == "POST":
        name = request.form.get("name").strip()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password").strip()

        if not name or not email or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        db = get_db()
        try:
            db.execute(
                "INSERT INTO students (name, email, password) VALUES (?, ?, ?)",
                (name, email, password),
            )
            db.commit()
        except Exception:
            flash("Email already registered.", "error")
            return redirect(url_for("register"))

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    user = get_current_user()
    if request.method == "POST":
        email = request.form.get("email").strip().lower()
        password = request.form.get("password").strip()

        db = get_db()
        cur = db.execute(
            "SELECT id, name, email, password FROM students WHERE email = ?",
            (email,),
        )
        row = cur.fetchone()

        if row and row["password"] == password:
            session["user_id"] = row["id"]
            session["user_name"] = row["name"]
            session["user_email"] = row["email"]
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html", user=user)


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.", "info")
    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)


@app.route("/courses", methods=["GET", "POST"])
def courses():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    db = get_db()

    if request.method == "POST":
        course_id = request.form.get("course_id")
        if course_id:
            try:
                db.execute(
                    "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)",
                    (user["id"], course_id),
                )
                db.commit()
                flash("Course registered successfully.", "success")
            except Exception:
                flash("You are already registered for this course.", "error")
        return redirect(url_for("courses"))

    # List courses and show if user is enrolled
    cur = db.execute(
        """
        SELECT c.id, c.code, c.title, c.credits,
               CASE WHEN e.id IS NULL THEN 0 ELSE 1 END AS is_enrolled
        FROM courses c
        LEFT JOIN enrollments e
            ON c.id = e.course_id AND e.student_id = ?
        ORDER BY c.code
        """,
        (user["id"],),
    )
    courses = cur.fetchall()

    return render_template("courses.html", user=user, courses=courses)


@app.route("/my-courses")
def my_courses():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    db = get_db()
    cur = db.execute(
        """
        SELECT c.code, c.title, c.credits
        FROM enrollments e
        JOIN courses c ON e.course_id = c.id
        WHERE e.student_id = ?
        ORDER BY c.code
        """,
        (user["id"],),
    )
    enrolled = cur.fetchall()

    return render_template("my_courses.html", user=user, courses=enrolled)


if __name__ == "__main__":
    ensure_database()
    app.run(debug=True)
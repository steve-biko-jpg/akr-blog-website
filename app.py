import os
from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
from db import get_connection


app = Flask(__name__)

# ---------------- Database Connection ----------------
def get_connection():
    """Connect to the database using environment variables for deployment."""
    return pymysql.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD", "STeVe!@a#kr5239"),
        database=os.environ.get("DB_NAME", "akrblog"),
        cursorclass=pymysql.cursors.DictCursor
    )

# ---------------- Dynamic Pages ----------------
def get_posts_by_category(category):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE category=%s ORDER BY created_at DESC", (category,))
            posts = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        posts = []
    finally:
        if 'conn' in locals():
            conn.close()
    return posts

@app.route("/")
def home():
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 5")
            posts = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        posts = []
    finally:
        if 'conn' in locals():
            conn.close()
    return render_template("home.html", posts=posts)

@app.route("/news")
def news():
    posts = get_posts_by_category("news")
    return render_template("news.html", posts=posts)

@app.route("/sport")
def sport():
    posts = get_posts_by_category("sport")
    return render_template("sport.html", posts=posts)

@app.route("/editorial")
def editorial():
    posts = get_posts_by_category("editorial")
    return render_template("editorial.html", posts=posts)

@app.route("/entertainment")
def entertainment():
    posts = get_posts_by_category("entertainment")
    return render_template("entertainment.html", posts=posts)

@app.route("/media")
def media():
    posts = get_posts_by_category("media")
    return render_template("media.html", posts=posts)

@app.route("/features")
def features():
    posts = get_posts_by_category("features")
    return render_template("features.html", posts=posts)

@app.route("/photos")
def photos():
    posts = get_posts_by_category("photos")
    return render_template("photos.html", posts=posts)

@app.route("/lifestyle")
def lifestyle():
    posts = get_posts_by_category("lifestyle")
    return render_template("lifestyle.html", posts=posts)

@app.route("/jobs")
def jobs():
    posts = get_posts_by_category("jobs")
    return render_template("jobs.html", posts=posts)

@app.route("/education")
def education():
    posts = get_posts_by_category("education")
    return render_template("education.html", posts=posts)

@app.route("/events")
def events():
    posts = get_posts_by_category("events")
    return render_template("events.html", posts=posts)

# ---------------- Static Pages ----------------
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/membership")
def membership():
    return render_template("membership.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/post/<int:post_id>")
def post(post_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts WHERE id=%s", (post_id,))
            post = cursor.fetchone()
    finally:
        conn.close()

    return render_template("post.html", post=post)

app.secret_key = "supersecretkey123"   # Change this later

# ========== ADMIN LOGIN ==========
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM admins WHERE username=%s AND password=SHA2(%s, 256)",
                (username, password)
            )
            admin = cursor.fetchone()
        conn.close()

        if admin:
            session["admin"] = admin["username"]
            return redirect("/admin")
        else:
            return render_template("admin_login.html", error="Invalid credentials")

    return render_template("admin_login.html")


# ========== ADMIN DASHBOARD ==========
@app.route("/admin")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin/login")

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts ORDER BY created_at DESC")
        posts = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", posts=posts)


# ========== ADD POST ==========
@app.route("/admin/add", methods=["GET", "POST"])
def admin_add():
    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO posts (title, content, category) VALUES (%s, %s, %s)",
                (title, content, category)
            )
            conn.commit()
        conn.close()

        return redirect("/admin")

    return render_template("admin_add.html")


# ========== EDIT POST ==========
@app.route("/admin/edit/<int:id>", methods=["GET", "POST"])
def admin_edit(id):
    if "admin" not in session:
        return redirect("/admin/login")

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id=%s", (id,))
        post = cursor.fetchone()

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        category = request.form["category"]

        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE posts SET title=%s, content=%s, category=%s WHERE id=%s",
                (title, content, category, id)
            )
            conn.commit()
        conn.close()
        return redirect("/admin")

    conn.close()
    return render_template("admin_edit.html", post=post)


# ========== DELETE POST ==========
@app.route("/admin/delete/<int:id>")
def admin_delete(id):
    if "admin" not in session:
        return redirect("/admin/login")

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM posts WHERE id=%s", (id,))
        conn.commit()
    conn.close()

    return redirect("/admin")


# ========== LOGOUT ==========
@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect("/admin/login")



# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

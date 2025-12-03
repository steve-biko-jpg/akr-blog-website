import os
from flask import Flask, render_template
import pymysql

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

# ---------------- Run App ----------------
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )

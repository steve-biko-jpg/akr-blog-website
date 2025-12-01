from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/news")
def news():
    return render_template("news.html")

@app.route("/sport")
def sport():
    return render_template("sport.html")

@app.route("/editorial")
def editorial():
    return render_template("editorial.html")

@app.route("/entertainment")
def entertainment():
    return render_template("entertainment.html")

@app.route("/media")
def media():
    return render_template("media.html")

@app.route("/features")
def features():
    return render_template("features.html")

@app.route("/photos")
def photos():
    return render_template("photos.html")

@app.route("/lifestyle")
def lifestyle():
    return render_template("lifestyle.html")

@app.route("/jobs")
def jobs():
    return render_template("jobs.html")

@app.route("/education")
def education():
    return render_template("education.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/events")
def events():
    return render_template("events.html")

@app.route("/membership")
def membership():
    return render_template("membership.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)

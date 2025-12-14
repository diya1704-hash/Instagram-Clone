from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from db import get_db_values
import os

app = Flask(__name__)
app.secret_key = "secretkey"

# Folder for uploads
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ---------------- SIGNUP ----------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        db = get_db_values()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",
            (username, email, password)
        )
        db.commit()
        return redirect("/login")
    return render_template("signup.html")

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form.get("password")
        db = get_db_values()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["profile_pic"] = user["profile_pic"]
            return redirect("/feed")
        return "Invalid credentials"
    return render_template("login.html")

# ---------------- UPLOAD PROFILE PIC ----------------
@app.route("/upload_profile", methods=["GET", "POST"])
def upload_profile():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        file = request.files.get("profile_pic")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            profile_url = "/" + filepath.replace("\\", "/")
            db = get_db_values()
            cur = db.cursor()
            cur.execute("UPDATE users SET profile_pic=%s WHERE id=%s", (profile_url, session["user_id"]))
            db.commit()
            session["profile_pic"] = profile_url
            return redirect("/feed")
        else:
            return "Invalid file"
    return render_template("upload_profile.html")

# ---------------- CREATE POST ----------------
@app.route("/create", methods=["GET", "POST"])
def create():
    if "user_id" not in session:
        return redirect("/login")
    if request.method == "POST":
        file = request.files.get("image_file")
        caption = request.form.get("caption")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            image_url = "/" + filepath.replace("\\", "/")
            db = get_db_values()
            cur = db.cursor()
            cur.execute(
                "INSERT INTO posts(user_id,image_url,caption) VALUES (%s,%s,%s)",
                (session["user_id"], image_url, caption)
            )
            db.commit()
            return redirect("/feed")
        return "Invalid file"
    return render_template("createpost.html")

# ---------------- FEED ----------------
@app.route("/feed")
def feed():
    if "user_id" not in session:
        return redirect("/login")
    db = get_db_values()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT posts.*, users.username, users.profile_pic
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.created_at DESC
    """)
    posts = cur.fetchall()
    for post in posts:
        cur.execute("""
            SELECT comments.text, users.username
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.post_id = %s
        """, (post['id'],))
        post['comments'] = cur.fetchall()
    return render_template("feed.html", posts=posts)

# ---------------- LIKE ----------------
@app.route("/like/<int:post_id>")
def like(post_id):
    if "user_id" not in session:
        return redirect("/login")
    db = get_db_values()
    cur = db.cursor()
    cur.execute("INSERT IGNORE INTO likes (user_id, post_id) VALUES (%s,%s)", (session["user_id"], post_id))
    db.commit()
    return redirect("/feed")

#COMMENT
@app.route("/comment/<int:post_id>", methods=["POST"])
def comment(post_id):
    if "user_id" not in session:
        return redirect("/login")
    text = request.form.get("comment")
    db = get_db_values()
    cur = db.cursor()
    cur.execute("INSERT INTO comments(user_id, post_id, text) VALUES (%s,%s,%s)", (session["user_id"], post_id, text))
    db.commit()
    return redirect("/feed")

#LOGOUT 
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)

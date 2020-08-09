import os
import sqlite3
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


app.secret_key = 'secretkey123'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.errorhandler(404)
def page_not_found(e):
  return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template("home/index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/add-modify')
def add_modify():
    return render_template("add-modify.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/school_details')
def school_details():
    con = sqlite3.connect("site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from School_Table")
    rows = cur.fetchall()
    return render_template("school_details.html", rows=rows)


@app.route('/schools')
def schools():
    con = sqlite3.connect("site.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Teacher_details")
    rows = cur.fetchall()
    return render_template("schools.html", rows=rows)


@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route('/')
def root():
    return render_template('home/index.html')

@app.route("/teacher")
def teacher_home():
    return render_template('teacher/index.html', title='Teacher')


@app.route("/settings")
def teacher_settings():
    return render_template('teacher/setting.html', title='Teacher')

@app.route("/explore")
def teacher_explore():
    return render_template('teacher/explore.html', title='Teacher')


@app.route("/certificate")
def teacher_certificate():
    return render_template('teacher/certificate.html', title='Teacher')

@app.route("/feedback")
def teacher_feedback():
    return render_template('teacher/feedback.html', title='Teacher')

@app.route("/course_modules")
def course_modules():
    return render_template('teacher/courses.html', title='Teacher')

@app.route("/dashboard")
def dasboard_index():
    return render_template('dashboard.html', title='Teacher')

@app.route("/profile")
def teacher_profile():
    return render_template('teacher/profile.html', title='Teacher')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/parent")
def parent():
    return render_template('parent.html', title='Parent')

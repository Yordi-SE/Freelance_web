from flask import Flask, render_template, url_for, redirect, flash, send_from_directory
from sqlalchemy.exc import IntegrityError
from model import storage, app, bcrypt
from werkzeug.utils import secure_filename
from model.form import RegistrationForm, LoginForm, UpdateForm, UploadCv, PostForm
import os
from model.base_model import User, Jobs
from flask_login import login_user, login_required, current_user, logout_user
from flask import request


@app.route("/")
@login_required
def home():
    obj = storage.job()
    title='Home'

    return render_template('home.html', obj=obj, title=title)

@app.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('home')
        flash('Your are already registered', 'success')
        return redirect(next)
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user1 = User(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data, birthdate=form.birthdate.data, password=hashed_password)

        storage.new(user1)
        storage.save()
        flash('Account created for {} {}'.format(form.first_name.data, form.last_name.data), 'success')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('home')
        return redirect(next)
    form = LoginForm()  
    if form.validate_on_submit():
        
        user = storage.query_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password,  form.password.data):
            flash('logged in successfully', 'success')
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('home')
            return redirect(next)
        else:
            flash('Incorrect password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route("/account", methods=['POST', 'GET'])
@login_required
def account():
    form = UploadCv()
    if form.validate_on_submit():
        pdf_file = form.cv.data
        filename = secure_filename(pdf_file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(filepath)
        if current_user.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.filename)
            os.remove(file_path)
        current_user.filename = filename
        storage.save()
        flash('file uploaded successfully!', 'success')
        return redirect(url_for('account'))
    return render_template('account.html', form=form, title='Account')

@app.route("/update", methods={'POST', 'GET'})
@login_required
def update():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        current_user.birthdate = form.birthdate.data
        current_user.phone = form.phone.data
        storage.save()
        flash('Updated successfully!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.birthdate.data =  current_user.birthdate
        form.phone.data = current_user.phone

    return render_template('update.html', form=form, title='Update')

@app.route("/download")
@login_required
def download():
    return send_from_directory(app.config['UPLOAD_FOLDER'], current_user.filename)

@app.route("/post", methods=['POST', 'GET'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data, job_type=form.job_type.data, location=form.location.data, level=form.level.data, vacancies=form.vacancies.data, salary=form.salary.data, deadline=form.deadline.data, description=form.description.data, user_email=form.email.data)
        storage.new(job)
        storage.save()
        flash("Job post successfully!", "success")
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

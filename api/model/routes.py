from flask import Flask, render_template, url_for, redirect, flash, send_from_directory, abort
from sqlalchemy.exc import IntegrityError
from model import storage, app, bcrypt
from werkzeug.utils import secure_filename
from model.form import RegistrationForm, LoginForm, UpdateForm, UploadCv, PostForm, PostEditForm
import os
from model.base_model import User, Jobs
from flask_login import login_user, login_required, current_user, logout_user
from flask import request


@app.route("/", methods=['POST', 'GET'])
@login_required
def home():

    if request.form:
        query = request.form.get('query')
        jobs = storage.query_job_title(query)
        
    lim = 5
    page = request.args.get('page', 1, type=int)
    obj = storage.query_page(page, lim)
    nu = storage.job()
    num_of_row = nu.count()
    if num_of_row % lim == 0:
        num_of_page = (num_of_row // lim)
    else:
        num_of_page = (num_of_row // lim) + 1
    page_range = 2
    available_pages = []
    for p in range(max(1, page - page_range), min(num_of_page + 1, page + page_range + 1)):
        available_pages.append(p)

  
    title='Home'
    if request.form:
        query = request.form.get('query')
        obj = storage.query_job_title(query)
        if not obj:
            abort(404)
        else:
            return render_template('home.html', obj=obj, title=title, page=page, num_of_page=num_of_page, num_of_row=num_of_row, available_pages=available_pages)

    return render_template('home.html', obj=obj, title=title, page=page, num_of_page=num_of_page, num_of_row=num_of_row, available_pages=available_pages)

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
    jobs = storage.query_email_job(current_user.email)

    form = UploadCv()
    if form.validate_on_submit():
        pdf_file = form.cv.data
        filename = '({})_{}'.format(current_user.id, secure_filename(pdf_file.filename))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if current_user.filename:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], current_user.filename)
            os.remove(file_path)
        pdf_file.save(filepath)
        current_user.filename = filename
        storage.save()
        flash('file uploaded successfully!', 'success')
        return redirect(url_for('account'))
    return render_template('account.html', form=form, title='Account', jobs=jobs)

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
def serve_file():
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

@app.route("/post/<int:post_id>")
@login_required
def postId(post_id):
    objs = storage.query_job(post_id)
    if objs:
        return render_template('edit_post.html', title=objs.title, objs=objs)
    abort(404)

@app.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
@login_required
def post_update(post_id):
    objs = storage.query_job(post_id)
    if objs:
        if objs.user_email != current_user.email:
            return render_template('forbiden.html')
    form = PostEditForm()
    print('form.errors')
    if form.validate_on_submit():
        objs.vacancies = form.vacancies.data
        objs.deadline = form.deadline.data
        objs.job_type = form.job_type.data
        objs.description = form.description.data
        objs.level = form.level.data
        objs.location = form.location.data
        objs.salary = form.salary.data
        objs.title = form.title.data
        storage.save()
        flash('You updated the successfully!', 'success')
        return redirect(url_for('postId', post_id=post_id))
    elif request.method == 'GET':
        form.vacancies.data = objs.vacancies
        form.deadline.data = objs.deadline
        form.job_type.data = objs.job_type
        form.description.data = objs.description
        form.level.data = objs.level
        form.location.data = objs.location
        form.title.data = objs.title
        form.salary.data = objs.salary
    return render_template('post_update.html', title='Update Post', form=form)

@app.route("/delete/<int:post_id>", methods=['POST', 'GET'])
@login_required
def delete(post_id):
    objs = storage.query_job(post_id)
    if objs:
        if request.method == 'GET':
            return render_template(url_for('postId', post_id=post_id), title=objs.title)
        if objs.user_email != current_user.email:
            return render_template('forbiden.html')
        else:
            storage.delete(objs)
            storage.save()
            flash('You deleted the post', 'danger')
            return redirect(url_for('home'))
    flash('Post not found', 'danger')
    return redirect(url_for('home'))

@app.route("/my_posts")
@login_required
def my_posts():
    lim = 5
    page = request.args.get('page', 1, type=int)
    obj = storage.query_page_email(current_user.email, page, lim)
    if not obj and page == 1:
        flash('You don\'t posts yet', 'danger')
        return redirect(url_for('home'))
    elif not obj:
        flash('No more posts', 'success')
    
    nu = storage.query_email_job(current_user.email)
    num_of_row = nu.count()
    if num_of_row % lim == 0:
        num_of_page = (num_of_row // lim)
    else:
        num_of_page = (num_of_row // lim) + 1
    page_range = 3
    available_pages = []
    for p in range(max(1, page - page_range), min(num_of_page + 1, page + page_range + 1)):
        available_pages.append(p)

    title='My Posts'

    return render_template('my_posts.html', obj=obj, title=title, page=page, num_of_page=num_of_page, num_of_row=num_of_row, available_pages=available_pages, page_range=page_range)


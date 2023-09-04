from flask import render_template, url_for, redirect, flash, send_from_directory, abort
from model import storage, blue
from werkzeug.utils import secure_filename
from model.form import PostForm, PostEditForm
import os
from model.base_model import Jobs
from flask_login import login_user, login_required, current_user, logout_user
from flask import request


@blue.route("/post", methods=['POST', 'GET'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        job = Jobs(title=form.title.data, job_type=form.job_type.data, location=form.location.data, level=form.level.data, vacancies=form.vacancies.data, salary=form.salary.data, deadline=form.deadline.data, description=form.description.data, user_email=current_user.email)
        storage.new(job)
        storage.save()
        flash("Job post successfully!", "success")
        return redirect(url_for('blue.home'))
    return render_template('post.html', form=form)

@blue.route("/post/<int:post_id>")
@login_required
def postId(post_id):
    applied = False
    user_job_id = storage.query_email_user_job(current_user.email)
    if user_job_id:
        for posts in user_job_id:
            if post_id in posts:
                applied = True
                break
    objs = storage.query_job(post_id)
    if objs:
        return render_template('edit_post.html', applied=applied, title=objs.title, objs=objs)
    abort(404)

@blue.route("/post/<int:post_id>/update", methods=['POST', 'GET'])
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
        return redirect(url_for('blue.postId', post_id=post_id))
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

@blue.route("/delete/<int:post_id>", methods=['POST', 'GET'])
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
            return redirect(url_for('blue.home'))
    flash('Post not found', 'danger')
    return redirect(url_for('blue.home'))

@blue.route("/my_posts")
@login_required
def my_posts():
    lim = 5
    page = request.args.get('page', 1, type=int)
    obj = storage.query_page_email(current_user.email, page, lim)
    if not obj and page == 1:
        flash('You don\'t posts yet', 'danger')
        return redirect(url_for('blue.home'))
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

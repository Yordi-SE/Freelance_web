from app import bcrypt
from flask import render_template, url_for, redirect, flash, send_from_directory, abort
from model import storage, blue
from werkzeug.utils import secure_filename
from model.form import LoginForm
from flask_login import login_user, login_required, current_user, logout_user
from flask import request



@blue.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('blue.home')
        return redirect(next)
    form = LoginForm()  
    if form.validate_on_submit():
        
        user = storage.query_email(form.email.data)
        if user and bcrypt.check_password_hash(user.password,  form.password.data):
            flash('logged in successfully', 'success')
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('blue.home')
            return redirect(next)
        else:
            flash('Incorrect password', 'danger')
    return render_template('login.html', title='Login', form=form)

@blue.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('blue.landing'))

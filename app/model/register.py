from app import bcrypt
from flask import render_template, url_for, redirect, flash, send_from_directory, abort
from model import storage, blue
from werkzeug.utils import secure_filename
from model.form import RegistrationForm
from model.base_model import User
from flask_login import login_user, login_required, current_user, logout_user
from flask import request



@blue.route("/register", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('blue.home')
        flash('Your are already registered', 'success')
        return redirect(next)
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user1 = User(first_name=form.first_name.data, last_name=form.last_name.data, phone=form.phone.data, email=form.email.data, birthdate=form.birthdate.data, password=hashed_password)

        storage.new(user1)
        storage.save()
        flash('Account created for {} {}'.format(form.first_name.data, form.last_name.data), 'success')
        return redirect(url_for('blue.login'))
    else:
        print(form.errors)
    return render_template('register.html', title='Register', form=form)
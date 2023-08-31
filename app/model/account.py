from app import app, mail
from flask import render_template, url_for, redirect, flash, send_from_directory, abort
from model import storage, blue
from werkzeug.utils import secure_filename
from model.form import UpdateForm, UploadCv
from model.base_model import Applied
import os
from flask_login import login_user, login_required, current_user, logout_user
from flask_mail import Message
from flask import request

def send_email(author,title):
    msg = Message('User Application on job {}'.format(title), sender="noreply@realyordanos.tech", recipients=[author])
    msg.body = """Applicant info:
Full name: {} {}
Email: {}
Phone: {}
Birthdate: {}
Cv: Please find the attached cv file
""".format(current_user.first_name, current_user.last_name, current_user.email, current_user.phone, current_user.birthdate)
    with app.open_resource('/home/ubuntu/Freelance/app/uploads/{}'.format(current_user.filename)) as pdf:
        msg.attach(filename='Applicant_cv.pdf', content_type='application/pdf', data=pdf.read())
    
    mail.send(msg)
    return 'Email sent'

@blue.route("/apply/<int:post_id>")
@login_required
def apply(post_id):
    objs = storage.query_job(post_id)
    applied = Applied(user_email=current_user.email, job_id=post_id)
    storage.new(applied)
    storage.save()
    feedback = send_email(objs.user_email, objs.title)
    if feedback == 'Email sent':
        flash("You applied for the job", "success")
    else:
        flash("Failed","warning")
        print("Failed")
    return redirect(url_for('blue.postId', post_id=objs.id))


@blue.route("/account", methods=['POST', 'GET'])
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
        return redirect(url_for('blue.account'))
    return render_template('account.html', form=form, title='account', jobs=jobs)

@blue.route("/update", methods={'POST', 'GET'})
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
        return redirect(url_for('blue.account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
        form.birthdate.data =  current_user.birthdate
        form.phone.data = current_user.phone

    return render_template('update.html', form=form, title='Update')

@blue.route("/download")
@login_required
def serve_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], current_user.filename)

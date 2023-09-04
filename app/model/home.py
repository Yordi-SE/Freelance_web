
from flask import render_template, send_from_directory, abort
from model import storage, blue
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, current_user, logout_user
from flask import request


@blue.route("/")
def landing():
    return render_template('landing_page.html')

@blue.route("/home", methods=['POST', 'GET'])
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

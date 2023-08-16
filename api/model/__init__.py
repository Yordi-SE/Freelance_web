from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'This&is&That'
UPLOAD_FOLDER = '/home/ubuntu/Freelance/api/model/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)





from model.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload()

@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    # print(exception)
    storage.close()

from model import routes
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

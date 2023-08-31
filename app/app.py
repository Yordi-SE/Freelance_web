from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY']
UPLOAD_FOLDER =
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 
app.config['MAIL_PASSWORD'] = 

mail = Mail(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


login_manager.login_view = 'blue.login'
login_manager.login_message_category = 'info'




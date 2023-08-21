from model.engine.db_storage import DBStorage
storage = DBStorage()
storage.reload()

from flask import Blueprint


blue = Blueprint('blue', __name__)



import model.account
import model.home
import model.login
import model.post
import model.register
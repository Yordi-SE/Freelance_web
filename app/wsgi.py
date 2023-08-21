from model import storage, blue

from app import app
app.register_blueprint(blue)
@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    # print(exception)
    storage.close()


if __name__ == '__main__':
    app.run(debug=True)
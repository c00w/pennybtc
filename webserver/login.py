from flask import Flask, render_template, abort, send_from_directory, make_response
app = Flask(__name__, template_folder='../templates', 
            static_folder = '../static')
app.Debug = True
app.secret_key = '#$%^&%$#%^&^$#%^%$%^&%$^&^%^%^%^ASD'

from flaskext.login import *

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.setup_app(app)

import users

import traceback, os

@app.teardown_request
def teardown_request_wrap(exception):
    teardown_request(exception)

def teardown_request(exception):
    if exception:
        traceback.print_exc()
        return 'Server Error'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, '../static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')
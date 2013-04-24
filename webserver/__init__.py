from flask import Flask, render_template, abort, send_from_directory, make_response
app = Flask(__name__, template_folder='../templates', 
            static_folder = '../static')
app.Debug = True

import traceback, posts, os, about

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
        

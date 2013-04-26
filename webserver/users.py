from webserver import *
import hashlib, json, os
from recaptcha.client import captcha

class User():
    def __init__(self, userid):
        self.userid = userid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.userid

def hash_password(password, salt):
    """
    Super secure hash function.
    Make sure that the salt is at least 512bits.
    """
    return hashlib.sha512(
                        hashlib.sha512(
                            str(password) + salt
                             ).hexdigest() + salt
                        ).hexdigest()

def check_user(username, password):
    """
    Salts and hashes the password and compares it to the stored one.
    """
    user = g.db.get('userid_' + username)
    if not user:
        return False
    else:
        user = json.loads(user)
    salt = user['salt']
    salt_password = hash_password(password, salt)
    if salt_password == user['password_hash']:
        return True
    return False

def make_user(username, password):
    """
    Makes a new user
    Returns true on success and false on failure
    """
    user = g.db.get('userid_' + username)
    if user:
        return False

    #No user, create a new user object.
    user = {'userid':username.encode('utf-8'),
            'salt':str(os.urandom(512/8)).encode("hex"),
           }

    #hash and store the password
    user['password_hash'] = hash_password(password, user['salt'])

    #Store user
    print g.db.set('userid_' + username, json.dumps(user))

    #Balances
    print g.db.set('userid_' + username + '_credit_balance', 1)
    print g.db.set('userid_' + username + '_btc_balance', 0)

    return True

@login_manager.user_loader
def load_user(userid):
    return User(userid)

def load_user_object(userid):
    return User(userid)

@app.route("/register/", methods=['POST','GET'])
def register():

    #Handle registration
    if request.method == 'POST':

        username = request.form.get('username', None)
        password = request.form.get('password', None)
        challenge = request.form.get('recaptcha_challenge_field', '')
        response = request.form.get('recaptcha_response_field', '')

        #Google Recaptcha
        response = captcha.submit(
            challenge,
            response,
            '6LdcwckSAAAAAGFCGW1Q4F0A7gkp43AzyTsHVkJh',
            request.remote_addr,
            )

        #Check for username and passwords
        if username and password and response.is_valid:

            #Actually do the db mucking
            ok = make_user(username, password)
            if not ok:
                return render_template("register.html")
            else:
                return redirect("/login/")

    return render_template("register.html", logged_in = not current_user.is_anonymous())

@app.route("/login/", methods=['POST','GET'])
def login():
    #Handle logins
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        #Check for valid passwords and usernames in db.
        if username and password:
            if check_user(username, password):
                login_user(User(username))
                return redirect("/user/")

    return render_template("login.html", logged_in = not current_user.is_anonymous())

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect("/")

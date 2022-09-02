from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import login_manager, LoginManager, UserMixin, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from pyravendb.store import document_store
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

# sudo /opt/lampp/lampp start
# sudo /opt/lampp/lampp stop

store = document_store.DocumentStore(urls=["http://localhost:8080"], database="gestorObra")
store.initialize()

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'


class User(UserMixin):
    def __init__(self, id, name, email, password, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_admin = is_admin
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return '<User {}>'.format(self.email)

@app.route('/login')
def login ():
    data = []
    return render_template('login.html', contacts=data)


@app.route('/')
def index ():
    data = []
    return render_template('index.html', contacts=data)

current_user = User("asd110","brian","a@a.com","1221321")



if __name__=="__main__":
        app.run(port=3000,debug=True)
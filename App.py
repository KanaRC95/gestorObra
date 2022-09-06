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

class Material:
    def __init__(self, name, cant, unit, type, proveedor, contacto):
        self.name = name
        self.unit = unit
        self.contacto = contacto
        self.cant = cant
        self.type = type
        self.proveedor = proveedor

def login ():
    data = []
    return render_template('login.html', contacts=data)


@app.route('/')
def index ():
    data = []
    return render_template('index.html', contacts=data)

@app.route('/materiales')
def mats ():
    data = []
    return render_template('materiales.html', contacts=data)
current_user = User("asd110","brian","a@a.com","1221321")


def queryObject(self):
    with store.open_session() as session:
        matList = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "year", "rating")  # Project
        )
    store.close()
    return pelisList

if __name__=="__main__":
        app.run(port=3000,debug=True)
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
data = []

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
    def __init__(self, name, unit, type, proveedor, contacto):
        self.name = name
        self.unit = unit
        self.contacto = contacto
        self.type = type
        self.proveedor = proveedor

    def getName(self):
        return self.name

    def getUnit(self):
        return self.unit

    def getCon(self):
        return self.contacto

    def getType(self):
        return self.type

    def getSource(self):
        return self.proveedor

def login ():
    data = []
    return render_template('login.html', contacts=data)


@app.route('/')
def index ():
    return render_template('index.html', data=data)

@app.route('/mats')
def mats ():
    temp =[]
    data = []
    mats = queryMats()
    for x in mats:
        temp.append(x.getName())
        temp.append(x.getUnit())
        temp.append(x.getType())
        temp.append(x.getSource())
        temp.append(x.getCon())
        data.append(temp)
        temp = []
    print(data)
    return render_template('materiales.html', mats=data)


@app.route('/add_mat', methods=['POST'])
def add_mats():
    if request.method == 'POST':
        name = request.form['mname']
        units = request.form['units']
        tipo = request.form['type']
        proveedor = request.form['source']
        contacto = request.form['pcont']

        material = Material(name,units,tipo,proveedor,contacto)
        with store.open_session() as session:
            session.store(material)
            session.save_changes()
            store.close()
        return redirect(url_for('mats'))

def queryMats():
    with store.open_session() as session:
        matList = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "unit", "contacto", "type", "proveedor")  # Project
        )
    store.close()
    return matList

if __name__=="__main__":
        app.run(port=3000,debug=True)
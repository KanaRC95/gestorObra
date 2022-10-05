import flask
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from pyravendb.store import document_store
from werkzeug.security import check_password_hash, generate_password_hash


# sudo /opt/lampp/lampp start
# sudo /opt/lampp/lampp stop

store = document_store.DocumentStore(urls=["http://localhost:8080"], database="gestorObra")
store.initialize()

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager()
login_manager.init_app(app)
current_user = ''
data = []

class User():
    def __init__(self, id, name, email, password, auth= True, active= True, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.auth = auth
        self.active = active
        self.is_admin = is_admin
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def is_authenticated(self):
        return self.auth
    def is_active(self):
        return self.active
    def get_id(self):
        return  self.id
    def __repr__(self):
        return '<User {}>'.format(self.email)



class Material:
    def __init__(self, name, unit, type, price, proveedor, contacto):
        self.name = name
        self.unit = unit
        self.type = type
        self.price = price
        self.proveedor = proveedor
        self.contacto = contacto


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
    def getPrice(self):
        return self.price

user = User('Kana','Brian','a@a.com','12345',True)

def addObject(obj):
    with store.open_session() as session:
        session.store(obj)
        session.save_changes()
        store.close()

@app.route('/')
def inicio():
    return render_template('index.html', data=data)

@app.route('/feats')
def feats():
    addObject(user)
    return render_template('login.html', data=data)

@login_manager.user_loader
def load_user(user_id):
    user = queryUser(user_id)
    return user[0]

@app.route('/index')
@login_required
def index ():
    return render_template('index.html', data=data)
@app.route('/mats')
@login_required
def mats ():
    temp =[]
    data = []
    mats = queryMats()
    for x in mats:
        temp.append(x.getName())
        temp.append(x.getUnit())
        temp.append(x.getType())
        temp.append(x.getPrice())
        temp.append(x.getSource())
        temp.append(x.getCon())
        data.append(temp)
        temp = []
    print(data)
    return render_template('materiales.html', mats=data)

@login_manager.unauthorized_handler
def unauthorized():
    return render_template('error.html')

@app.route('/add_mat', methods=['POST'])
def add_mats():
    if request.method == 'POST':
        name = request.form['mname']
        units = request.form['units']
        tipo = request.form['type']
        precio = request.form['price']
        proveedor = request.form['source']
        contacto = request.form['pcont']

        material = Material(name,units,tipo,precio, proveedor,contacto)
        addObject(material)
        return redirect(url_for('mats'))
@app.route('/login')
def loginScreen():
    return flask.render_template('login.html', form=data)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/logear', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        clave = request.form['pass']
        users = queryUsers(username,clave)

        if not users:
            print('No hay usuarios')
            return flask.render_template('error.html', form=data)
        else:
            login_user(users[0])
            current_user = users[0]
            return flask.render_template('homescreen.html', form=data)




def queryMats():
    with store.open_session() as session:
        matList = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "unit", "contacto", "type","price", "proveedor")  # Project
        )
    store.close()
    return matList

def queryUsers(name,password):
    with store.open_session() as session:
        userList = list(  # Materialize query
            session
            .query(object_type=User)  # Query for Products
            .where_equals("name",name) # Filter
            # .skip(0).take(10)                       # Page
            .select("id","name")  # Project
        )
    store.close()
    return userList

def queryUser(id):
    with store.open_session() as session:
        userList = list(  # Materialize query
            session
            .query(object_type=User)  # Query for Products
            .where_equals("id",id) # Filter
            # .skip(0).take(10)                       # Page
            .select("id","name")  # Project
        )
    store.close()
    return userList


if __name__=="__main__":
        app.run(port=3000,debug=True)

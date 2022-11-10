import flask
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from pyravendb.store import document_store
from classes import *
from methods import *

from werkzeug.security import check_password_hash, generate_password_hash


# sudo /opt/lampp/lampp start
# sudo /opt/lampp/lampp stop



app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager()
login_manager.init_app(app)
current_user = ''
data = []
budget = []
budgetO = []
TOTAL = 0
title = ''
BINDEX = -1



user = User('Kana','Brian','a@a.com','12345',True)



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

@app.route('/home')
@login_required
def home ():
    return render_template('homescreen.html', data=data)
@app.route('/mats')
@login_required
def rmats():
    data = mats()
    return render_template('materiales.html', mats=data)

@app.route('/jobs')
@login_required
def rjobs():
    data = jobs()
    data2 = mats()
    return render_template('trabajos.html', jobs=data, mats=data2)

@app.route('/clients')
@login_required
def cl():
    data = clients()
    return render_template('clients.html', clients=data)

@app.route('/pres')
@login_required
def bgt():
    data = jobs()
    return render_template('pres.html', jobs=budget, mats=data, total=TOTAL)
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

        material = Material(name,units,tipo,precio, proveedor,contacto,current_user)
        addObject(material)
        return redirect(url_for('rmats'))

@app.route('/add_client', methods=['POST'])
def add_client():
    if request.method == 'POST':
        name = request.form['cname']
        contacto = request.form['ccont']
        client = Cliente(name,contacto)
        addObject(client)
        return redirect('/clients')

@app.route('/add_job', methods=['POST'])
def add_job():
    if request.method == 'POST':
        name = request.form['tname']
        precio = request.form['tprice']
        desc = request.form['tdesc']
        materiales = []

        trabajo = Trabajo(name,precio, desc, materiales)
        addObject(trabajo)
        data = jobs()
        return render_template('trabajos.html', jobs=data, mats=data)

@app.route('/details', methods=['GET','POST'])
def deets():
    invoice()
    return render_template('invoice.html')

@app.route('/add_pres/<name>', methods=['POST','GET'])
def add_pres(name):
    global TOTAL, BINDEX
    temp = []
    js = queryJobsL(name)
    BINDEX += 1
    for x in js:
        budgetO.append(x)
        TOTAL += int(x.getPrice())
        temp.append(BINDEX)
        temp.append(x.getName())
        temp.append(x.getPrice())
        temp.append(x.getDesc())
        budget.append(temp)
        temp = []
    return redirect('/pres')
    #return flask.render_template('pres.html', jobs=budget, mats=data, total=TOTAL)

@app.route('/add_mat_tojob/<name>', methods=['POST','GET'])
def addM_toJ(name):
    global title
    mat = queryMatsN(name)
    job = queryJobsL(title)

    with store.open_session() as session:
        job[0].addMaterial(mat)
        session.save_changes()
        store.close()

    return redirect('/jobs')

@app.route('/delete/<id>', methods=['POST','GET'])
def del_pres(id):
    global TOTAL, BINDEX
    BINDEX -= 1
    TOTAL -= int(budget[int(id)][2])
    budget.pop(int(id))
    budgetO.pop(int(id))
    return redirect('/pres')

@app.route('/edit_job/<id>', methods=['POST','GET'])
def addM_toJob(id):
    global title
    title = id
    dataM = mats()
    return flask.render_template('job_edit.html', title=title, mats=dataM)

@app.route('/save', methods=['GET','POST'])
def save():
    pres = Presupuesto('test',current_user,budget)
    addObject(pres)
    return redirect('/home')
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





if __name__=="__main__":
        app.run(port=3000,debug=True)

import datetime
from collections import *
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
currentP = ''
currentPy = ''
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
    print(current_user)
    return render_template('homescreen.html', data=data)

@app.route('/info')
@login_required
def info ():
    print(current_user)
    return render_template('data.html', data=data)

@app.route('/mats')
@login_required
def rmats():
    data = mats()
    return render_template('materiales.html', mats=data)

@app.route('/pers')
@login_required
def rpers():
    data = personnel()
    return render_template('personal.html', obr=data)

@app.route('/jobs')
@login_required
def rjobs():
    data = jobs()
    return render_template('trabajos.html', jobs=data)

@app.route('/cjobs')
@login_required
def cjobs():
    dataM = mats()
    return render_template('cargaJobs.html', mats=dataM)


@app.route('/clients')
@login_required
def cl():
    data = clients()
    return render_template('clients.html', clients=data)

@app.route('/pres')
@login_required
def bgt():
    pr = pres()
    cl = clients()
    return render_template('pres.html', pres=pr, clients=cl)

@app.route('/prov')
@login_required
def provs():
    pr = query(Proveedor)
    return render_template('prov.html', provs=pr)

@app.route('/proy')
@login_required
def proy():
    proys = proyL()
    return render_template('proyScreen.html', pys=proys)

@app.route('/cargaPres/<name>')
@login_required
def nbgt(name):
    global currentP
    currentP = name
    presE = queryPresL(name)
    jobsL = presE[0].getJobs()
    js = jobs()
    return render_template('cargaPres.html', pres=presE, jobs=js, listado=jobsL)

@app.route('/generarProy/<name>')
@login_required
def genProy(name):
    presE = queryPresL(name)
    #pname, Cliente, addr, MatsFaltantes, MatsDisponibles, Obreros, Capataz, fechaInicio, fechaFin,
    #Pedidos, TrabajosR, TrabajosD, budget
    pname = 'Proyecto '+presE[0].oname
    client = presE[0].Cliente
    addr = presE[0].addr
    tbjs = presE[0].Trabajos
    bgt = presE[0].budget
    datenow = datetime.datetime.now().strftime("%x")
    matList = []
    matN = matNames()
    for tb in tbjs:
        for tbs in tb['Materiales']:
         matList.append(tbs)
    res = {}
    for mt in matList:
        mt.pop('Proveedor')
        mt.pop('type')
        mt.pop('price')
        mt.pop('total')
        if mt['name'] in res.keys():
            res[mt['name']]+=mt['cant']
        else:
            res[mt['name']] = mt['cant']

    proy = Proyecto(pname,client,addr,res,None,None,None,datenow,None,None,tbjs,None,bgt,0,'Comenzado')
    addObject(proy)

    return redirect(url_for('proy'))

@app.route('/startJ/<name>/<proy>')
@login_required
def stJ(name,proy):
    py = queryP(Proyecto,proy)
    tr = ''
    datenow = datetime.datetime.now().strftime("%x")

    for x in py.TrabajosR:
        if x['name']==name:
            tr = x
            with store.open_session() as session:
                p = list(
                    session
                    .query(object_type=Proyecto)  # Query for Products
                    .where_equals("pname", proy)
                )
                p[0].movTR(x)
                session.save_changes()
            store.close()


    trP = TrabajoP(tr['name'],tr['Materiales'],tr['totalT'],None,datenow,None,py.pname)
    addObject(trP)
    return redirect(url_for('deetsProy', name = py.pname))

@app.route('/test')
@login_required
def testing():
    return redirect(url_for('home'))

@app.route('/deetsProy/<name>')
@login_required
def deetsProy(name):
    proy = queryProyL(name)
    global currentPy
    currentPy = proy
    trP = query(TrabajoP)
    obr = query(Obrero)
    prv = query(Proveedor)
    mt = query(Material)
    return render_template('gestionProy.html', data=proy, trps=trP, obrs=obr, prov=prv, mats=mt)

@app.route('/pend/<name>/<proy>')
@login_required
def penScr(name,proy):
    trp = queryTP(TrabajoP,name)
    p = queryP(Proyecto,proy)
    obr = query(Obrero)
    return render_template('pendiente.html', pr=p, tps=trp, obrs=obr)

@app.route('/pendC/<name>/<proy>')
@login_required
def compTR(name, proy):
    #chequear materiales disponibles
    m = {}
    p = queryP(Proyecto,proy)
    with store.open_session() as session:
        trp = list(  # Materialize query
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("tpname", name)  # Filter
        )
        p = list(
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname", proy)
        )
        obr = list(session.query(object_type=Obrero))
        for x in trp[0].Materiales:
            m[x['name']]=x['cant']
        pm = p[0].MatsDisponibles
        err = []
        if pm:
            for key in pm.keys():
                #pm: disponibles, m: necesarios
                if key in m.keys():
                    if pm[key] < m[key]:
                        e = 'No hay suficiente '+key+'.'
                        err.append(e)
        if not trp[0].Obreros:
            e = 'No hay Obreros asignados.'
            err.append(e)

        if not err:
            for key in p[0].MatsDisponibles.keys():
                if key in m.keys():
                    p[0].MatsDisponibles[key]-=m[key]

            trp[0].fechaFin = dateNow()
            p[0].compTR(trp[0]) #Hacer dict para que no guarde tan complejo
            session.delete_by_entity(trp[0])
            session.save_changes()
        else:
            return render_template('error.html', error=err)
    store.close()

    obr = query(Obrero)
    return redirect(url_for('deetsProy', name = p[0].pname))

@app.route('/assigOb/<job>/<name>/<py>')
@login_required
def addObr(job,name,py):
    p = queryP(Proyecto,py)
    global currentPy
    currentPy = p
    jobN = queryN(Trabajo,job).name
    with store.open_session() as session:
        qObr = list(
            session
            .query(object_type=Obrero)  # Query for Products
            .where_equals("name", name)
        )

        qTbs = list(
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("tpname", job)
        )
        qTbs[0].addObrero(qObr[0].name,qObr[0].occ, p.pname)
        qObr[0].addTrabajo(jobN,p.pname,dateNow())
        session.save_changes()
    store.close()
    return redirect(url_for('deetsProy', name = p.pname))


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('error.html')

@app.route('/add_mat', methods=['POST'])
@login_required
def add_mats():
    if request.method == 'POST':
        name = request.form['mname']
        tipo = request.form['type']
        precio = request.form['price']
        prov = Proveedor('Alberto', 'a@a.com','0985000111','Pilar')
        #(self, name, type, price, Proveedor, cant)
        material = Material(name,tipo,precio, prov,0)
        addObject(material)
        return redirect(url_for('rmats'))

@app.route('/add_pay/<name>', methods=['POST'])
@login_required
def add_pay(name):
    p = queryP(Proyecto, name)
    f = {}
    if request.method == 'POST':
        cuota = request.form['cuota']
        iva = request.form['iva']
        pago = request.form['paid']
        f['Cliente'] = p.Cliente['name']
        f['RUC'] = p.Cliente['ruc']
        f['Detalles'] = 'Materiales y Mano de Obra'
        f['IVA'] = iva
        f['Cuota'] = int(cuota)
        f['Valor'] = int(pago)
        with store.open_session() as session:
            p = list(
                session
                .query(object_type=Proyecto)  # Query for Products
                .where_equals("pname", name)
            )
            p[0].budget += int(pago)
            p[0].addFactura(f)
            session.save_changes()
        store.close()

        print(f)
        return redirect(url_for('deetsProy', name = p[0].pname))

@app.route('/add_ped/<name>', methods=['POST'])
@login_required
def add_pay(name):
    p = queryP(Proyecto, name)
    return redirect(url_for('deetsProy', name=p.pname))

@app.route('/add_prov', methods=['POST'])
@login_required
def add_prov():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        tel = request.form['phone']
        city = request.form['city']
        addr = request.form['addr']
        #(self, name, type, price, Proveedor, cant)
        p = Proveedor(name,email,tel,city,addr)
        addObject(p)

        return redirect(url_for('provs'))

@app.route('/add_pers', methods=['POST'])
@login_required
def add_pers():
    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        occ = request.form['occ']
        cont = request.form['cont']
        blood = request.form['blood']
        addr = request.form['addr']
        cont1 = request.form['cont1']
        cont2 = request.form['cont2']
        act = 'Si'
        jobs = []

        obr = Obrero(name, tel, occ, cont, blood, addr, cont1, cont2, act, jobs)
        addObject(obr)
        return redirect(url_for('rpers'))

@app.route('/add_pres', methods=['POST'])
@login_required
def add_pres():
    if request.method == 'POST':
        obra = request.form['oname']
        cl = request.form['client']
        addr = request.form['addr']
        jobs = []
        budget = 0
        status = 'Abierto'
        clName = cl.split("/")
        client = queryClient(clName[1])

        pres = Presupuesto(obra, client, addr, jobs, status, budget)
        addObject(pres)

    return redirect('/pres')


@app.route('/add_client', methods=['POST'])
@login_required
def add_client():
    if request.method == 'POST':
        name = request.form['cname']
        phone = request.form['cphone']
        addr = request.form['caddr']
        ruc = request.form['cruc']
        mail = request.form['cemail']
        city = request.form['ccity']
        type = request.form['ctype']

        client = Cliente(name,phone,addr,ruc,mail,city,type)
        addObject(client)
        return redirect('/clients')

@app.route('/add_job', methods=['POST'])
@login_required
def add_job():
    if request.method == 'POST':
        name = request.form['tname']
        precio = request.form['tprice']
        desc = request.form['tdesc']
        materiales = request.form.getlist("check")
        c = request.form.getlist("mcant")
        prov = Proveedor('Alberto', 'a@a.com', '0985000111', 'Pilar')
        cant = [s for s in c if s.strip()]
        jmats = []
        for m, c in zip(materiales,cant):
            q = queryMatsN(m)
            aux = q[0]
            #(self, name, type, price, Proveedor, cant)
            mat = Material(aux.getName(),aux.getType(),int(aux.getPrice()),prov,int(c))
            jmats.append(mat)
        total = 0
        for mat in jmats:
            total += int(mat.getTotal())


        trabajo = Trabajo(name,precio, total, (int(precio)+total) ,desc,jmats)
        addObject(trabajo)
        data = jobs()
        return render_template('trabajos.html', jobs=data)


@app.route('/details', methods=['GET','POST'])
@login_required
def deets():
    pres = presL(currentP)
    presE = queryPresL(currentP)
    jobsL = presE[0].getJobs()
    datenow = datetime.datetime.now().strftime("%x")
    return render_template('detalles.html', info=pres, listado=jobsL, fecha=datenow)

@app.route('/add_pr/<name>', methods=['POST','GET'])
@login_required
def add_pr(name):
    global currentP
    js = queryJobsL(name)
    print(currentP)
    with store.open_session() as session:
        pres = list(
            session
            .query(object_type=Presupuesto)  # Query for Products
            .where_equals("oname", currentP)
        )
        pres[0].addJob(js[0])
        pres[0].addBudget(js[0].totalT)
        session.save_changes()
    store.close()

    return redirect('/cargaPres/'+currentP)
    #return flask.render_template('cargaPres.html', jobs=budget, mats=data, total=TOTAL)

@app.route('/add_mat_tojob/<name>', methods=['POST','GET'])
@login_required
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
@login_required
def del_pres(id):
    global TOTAL, BINDEX
    BINDEX -= 1
    TOTAL -= int(budget[int(id)][2])
    budget.pop(int(id))
    budgetO.pop(int(id))
    return redirect('/pres')

@app.route('/edit_job/<id>', methods=['POST','GET'])
@login_required
def addM_toJob(id):
    job = queryJobsL(id)
    dataM = job[0].Materiales
    title = job[0].name
    return flask.render_template('job_edit.html', title=title, mats=dataM, job=job[0])

@app.route('/save', methods=['GET','POST'])
@login_required
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

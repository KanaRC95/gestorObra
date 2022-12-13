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
    data = query(Material)
    pr = query(Proveedor)
    return render_template('materiales.html', mats=data, provs=pr)

@app.route('/pers')
@login_required
def rpers():
    data = personnel()
    return render_template('personal.html', obr=data)

@app.route('/jobs')
@login_required
def rjobs():
    data = queryJobs()
    return render_template('trabajos.html', jobs=data)

@app.route('/cjobs')
@login_required
def cjobs():
    dataM = mats()
    prov = query(Proveedor)
    return render_template('cargaJobs.html', mats=dataM, provs=prov)


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

@app.route('/proyReport/<name>')
@login_required
def proyReport(name):
    with store.open_session() as session:
        p = list(
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname", name)
        )
        pend = list(
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("Proyecto", name)
        )
        if not pend:
            pend = []
        fReport = dateNow()
        session.save_changes()
    store.close()
    return render_template('proyReport.html', proy=p[0], inpro=pend, fr=fReport)

@app.route('/changeStatus/<name>')
@login_required
def cStatus(name):
    with store.open_session() as session:
        p = list(
            session
            .query(object_type=Presupuesto)  # Query for Products
            .where_equals("oname", name)
        )
        st = p[0].status
        if st=='Abierto':
            p[0].status='Cerrado'
        else:
            p[0].status='Abierto'
        session.save_changes()
    store.close()
    return redirect(url_for('bgt'))

@app.route('/assignCptz/<name>', methods=['POST'])
@login_required
def cptz(name):
    if request.method == 'POST':
        n = request.form['cap']
        cap = n.split(' / ',1)[0]
        ced = n.split(' / ',1)[1]

        with store.open_session() as session:
            p = list(
                session
                .query(object_type=Proyecto)  # Query for Products
                .where_equals("pname", name)
            )
            o = list(
                session
                .query(object_type=Obrero)  # Query for Products
                .where_equals("name", name)
                .where_equals("ced",ced)
            )
            p[0].Capataz=o[0]
            session.save_changes()
        store.close()

        return redirect(url_for('deetsProy', name=name))

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

    proy = Proyecto(pname,client,addr,res,None,None,None,datenow,None,None,tbjs,None,bgt,0,'Comenzado',None)
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
    return flask.render_template('test.html')

@app.route('/deetsProy/<name>')
@login_required
def deetsProy(name):
    proy = queryProyL(name)
    global currentPy
    currentPy = proy
    trP = queryTPr(TrabajoP,name)
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
            .where_equals("tpname",name)
            .where_equals("Proyecto",proy)  # Filter
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
        x = request.form['source']
        prov = x.split(" / ",1)[0]
        x = queryN(Proveedor,prov)
        #(self, name, type, price, Proveedor, cant)
        material = Material(name,tipo,precio, x,0)
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

        return redirect(url_for('deetsProy', name = p[0].pname))

@app.route('/add_ped/<name>', methods=['POST'])
@login_required
def add_ped(name):
    p = queryP(Proyecto, name)
    x = request.form['mat']
    mtname = x.split(' / ',1)[0]
    mat = queryN(Material,mtname)
    val = int(request.form['cant'])
    mat.cant = val
    mat.setTotal()
    if mat.total>p.budget:
        dif = (mat.total-p.budget)
        e = "No hay suficientes fondos. Se necesitan "+str(dif)+"Gs. adicionales"
        err = [e]
        return render_template('error.html', error=err)
    else:
        with store.open_session() as session:
            p = list(
                session
                .query(object_type=Proyecto)  # Query for Products
                .where_equals("pname", name)
            )

            if p[0].MatsDisponibles:
                keys =  p[0].MatsDisponibles.keys()
                if mat.name in keys:
                    p[0].MatsDisponibles[mat.name]+=val
                else:
                    p[0].MatsDisponibles[mat.name] = val
            else:
                m = {
                    mat.name: val
                }
                p[0].MatsDisponibles = m
            p[0].gastos += int(mat.total)
            p[0].budget -= int(mat.total)
            session.save_changes()
        store.close()
        return redirect(url_for('deetsProy', name=p[0].pname))


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
        ced = request.form['ced']
        cont = request.form['cont']
        blood = request.form['blood']
        addr = request.form['addr']
        cont1 = request.form['cont1']
        cont2 = request.form['cont2']
        act = 'Si'
        jobs = []

        obr = Obrero(name, tel, occ, ced, cont, blood, addr, cont1, cont2, act, jobs)
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
        md = request.form['med']
        materiales = request.form.getlist("check")
        c = request.form.getlist("mcant")
        cant = [s for s in c if s.strip()]
        jmats = []
        for m, c in zip(materiales,cant):
            q = queryMatsN(m)
            aux = q[0]
            #(self, name, type, price, Proveedor, cant)
            mat = Material(aux.getName(),aux.getType(),int(aux.getPrice()),'',int(c))
            jmats.append(mat)
        total = 0
        for mat in jmats:
            total += int(mat.getTotal())


        trabajo = Trabajo(name,int(precio), total, (int(precio)+total) ,desc,jmats)
        trabajo.medicion = md
        addObject(trabajo)
        return redirect(url_for('rjobs'))


@app.route('/details/<name>', methods=['GET','POST'])
@login_required
def deets(name):
    pres = queryPresL(name)
    jobsL = pres[0].Trabajos
    return render_template('detalles.html', info=pres[0], listado=jobsL, fecha=dateNow())

@app.route('/add_pr/<pr>', methods=['POST','GET'])
@login_required
def add_pr(pr):
    if request.method == 'POST':
        ct = int(request.form['cant'])
        jbname = request.form['jb']
        j = queryN(Trabajo,jbname)
        mats = j.Materiales
        totalT = 0

        for m in mats:
            m['cant'] *= ct
            m['total'] *= ct
            totalT += m['total']

        tb = {
            "name": j.name,
            "priceM": j.priceM * ct,
            "totalM": j.totalM * ct,
            "totalT": totalT+(j.priceM*ct),
            "desc": j.desc,
            "Materiales": mats,
            "Superficie": ct
        }
        with store.open_session() as session:
            pres = list(
                session
                .query(object_type=Presupuesto)  # Query for Products
                .where_equals("oname", pr)
            )
            pres[0].addJob(tb)
            pres[0].addBudget(totalT+(j.priceM*ct))
            session.save_changes()
        store.close()

    return redirect('/cargaPres/'+pres[0].oname)
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

@app.route('/delJ/<name>/<pres>', methods=['POST','GET'])
@login_required
def del_pres(name,pres):
    with store.open_session() as session:
        p = list(  # Materialize query
            session
            .query(object_type=Presupuesto)  # Query for Products
            .where_equals("oname", pres)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        for t in p[0].Trabajos:
            if name in t.values():
                p[0].budget-=t['totalT']
                t.clear()
        tl = p[0].Trabajos
        newtl = list(filter(None,tl))
        p[0].Trabajos = newtl
        session.save_changes()

    store.close()

    return redirect(url_for('nbgt', name = p[0].oname))

@app.route('/del_job/<name>', methods=['POST','GET'])
@login_required
def del_job(name):
    with store.open_session() as session:
        p = list(  # Materialize query
            session
            .query(object_type=Trabajo)  # Query for Products
            .where_equals("name", name)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        print(p)
        session.delete_by_entity(p[0])
        session.save_changes()

    store.close()

    return redirect(url_for('rjobs'))

@app.route('/del_mat/<name>', methods=['POST','GET'])
@login_required
def del_mat(name):
    with store.open_session() as session:
        p = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            .where_equals("name", name)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        session.delete_by_entity(p[0])
        session.save_changes()

    store.close()

    return redirect(url_for('rmats'))

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

import datetime
from collections import *
import flask
import flask_login
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




@app.route('/')
def inicio():
    return render_template('index.html', data=data)

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
    return render_template('data.html', data=data)

@app.route('/users')
def feats():
    usr = queryUrs()
    return render_template('users.html', data=usr)

@app.route('/mats')
@login_required
def rmats():
    data = query(Material, flask_login.current_user.id)
    pr = query(Proveedor, flask_login.current_user.id)
    return render_template('materiales.html', mats=data, provs=pr)

@app.route('/audits')
@login_required
def audits():
    data = query(Audit, flask_login.current_user.id)
    return render_template('audits.html', data=data)

@app.route('/pers')
@login_required
def rpers():
    data = query(Obrero,flask_login.current_user.id)
    return render_template('personal.html', obr=data)

@app.route('/jobs')
@login_required
def rjobs():
    data = query(Trabajo,flask_login.current_user.id)
    return render_template('trabajos.html', jobs=data)

@app.route('/cjobs')
@login_required
def cjobs():
    dataM = query(Material,flask_login.current_user.id)
    prov = query(Proveedor,flask_login.current_user.id)
    return render_template('cargaJobs.html', mats=dataM, provs=prov)

@app.route('/editUsrScreen/<id>')
@login_required
def edit_user(id):
    usr = queryUser(id)
    return render_template('usrEdit.html', user=usr[0])

@app.route('/edit_user/<id>', methods=['POST'])
@login_required
def edit_usr(id):
    if request.method == 'POST':
        name = request.form['name']
        mail = request.form['mail']
        pss = request.form['pass']
        with store.open_session() as session:
            usr = list(
                session
                .query(object_type=User)  # Query for Products
                .where_equals("id", id)
            )
            usr[0].name=name
            usr[0].email=mail
            usr[0].password=pss
            session.save_changes()
        store.close()
        return redirect(url_for('feats'))

@app.route('/clients')
@login_required
def cl():
    data = query(Cliente,flask_login.current_user.id)
    return render_template('clients.html', clients=data)

@app.route('/pres')
@login_required
def bgt():
    pr = query(Presupuesto,flask_login.current_user.id)
    cl = query(Cliente,flask_login.current_user.id)
    return render_template('pres.html', pres=pr, clients=cl)

@app.route('/prov')
@login_required
def provs():
    pr = query(Proveedor,flask_login.current_user.id)
    return render_template('prov.html', provs=pr)

@app.route('/proy')
@login_required
def proy():
    proys = query(Proyecto,flask_login.current_user.id)
    return render_template('proyScreen.html', pys=proys)

@app.route('/proyReport/<name>')
@login_required
def proyReport(name):
    with store.open_session() as session:
        p = list(
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname", name)
            .where_equals("User", flask_login.current_user.id)
        )
        pend = list(
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("Proyecto", name)
            .where_equals("User", flask_login.current_user.id)
        )

        if not pend:
            pend = []
        fReport = dateNow()
        fact = 0
        totalFact = 0

        for f in p[0].pagos:
            fact+=1
            totalFact+=f['MontoTotal']
        pagos = {
            "Cantidad":fact,
            "Suma":totalFact
        }
        session.save_changes()
    store.close()
    return render_template('proyReport.html', proy=p[0], inpro=pend, fr=fReport, pay=pagos)

@app.route('/finish/<name>')
@login_required
def finish(name):
    with store.open_session() as session:
        p = list(
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname", name)
            .where_equals("User", flask_login.current_user.id)
        )
        trp = list(
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("pname", name)
            .where_equals("User", flask_login.current_user.id)
        )
        if not trp and not p[0].TrabajosR:
            p[0].status = 'Finalizado'
        else:
            p[0].status = 'Interrumpido'
        p[0].fechaFin = dateNow()

        session.save_changes()
    store.close()
    return redirect(url_for('proyReport',name=p[0].pname))

@app.route('/changeStatus/<name>')
@login_required
def cStatus(name):
    with store.open_session() as session:
        data = list(
            session
            .query(object_type=Presupuesto)  # Query for Products
            .where_equals("oname", name)
        )
        for x in data:
            if x.User == flask_login.current_user.id:
                p=x
        st = p.status
        if st=='Abierto':
            p.status='Cerrado'
        else:
            p.status='Abierto'
        session.save_changes()
    store.close()
    return redirect(url_for('bgt'))

@app.route('/reopen/<name>')
@login_required
def reopen(name):
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
                .where_equals("User", flask_login.current_user.id)
            )
            o = list(
                session
                .query(object_type=Obrero)  # Query for Products
                .where_equals("name", name)
                .where_equals("ced",ced)
                .where_equals("User", flask_login.current_user.id)
            )
            p[0].Capataz=o[0]
            session.save_changes()
        store.close()
        return redirect(url_for('deetsProy', name=name))

@app.route('/cargaPres/<name>')
@login_required
def nbgt(name):
    presE = [queryPres(Presupuesto,name,flask_login.current_user.id)]
    jobsL = presE[0].Trabajos
    js = query(Trabajo,flask_login.current_user.id)
    return render_template('cargaPres.html', pres=presE, jobs=js, listado=jobsL)

@app.route('/generarProy', methods=["GET", "POST"])
@login_required
def genProy():
    if request.method == 'POST':
        cuota = request.form['cuota']
        iva = request.form['iva']
        name = request.form['pname']
        if iva == 'Sin IVA':
            valorIVA = 0
        elif iva == '10':
            valorIVA = 10
        else:
            valorIVA = 5

        presE = queryPres(Presupuesto,name,flask_login.current_user.id)
        #pname, Cliente, addr, MatsFaltantes, MatsDisponibles, Obreros, Capataz, fechaInicio, fechaFin,
        #Pedidos, TrabajosR, TrabajosD, budget
        pname = 'Proyecto '+presE.oname
        client = presE.Cliente
        addr = presE.addr
        tbjs = presE.Trabajos
        bgt = presE.budget
        datenow = datetime.datetime.now().strftime("%x")
        matList = []
        #matN = matNames()
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
        valorCuotas = bgt/int(cuota)
        montoIVA = valorCuotas/valorIVA
        pagos = []
        for i in range(int(cuota)):
            pago = {
                "Cliente": client['name'],
                "RUC": client['ruc'],
                "Detalles": "Materiales y Mano de Obra",
                "IVA": iva,
                "Cuota": (i+1),
                "MontoTotal": valorCuotas,
                "MontoIVA": montoIVA,
                "Estado": "Sin pagar"
            }
            pagos.append(pago)

        proy = Proyecto(pname,client,addr,res,None,None,None,datenow,None,None,tbjs,None,bgt,0,'Comenzado',pagos,0,flask_login.current_user.id)
        addObject(proy)

    return redirect(url_for('proy'))

@app.route('/startJ/<name>/<proy>')
@login_required
def stJ(name,proy):
    py = queryP(Proyecto,proy,flask_login.current_user.id)
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
                    .where_equals("User", flask_login.current_user.id)
                )
                p[0].movTR(x)
                session.save_changes()
            store.close()


    trP = TrabajoP(tr['name'],tr['Materiales'],None,tr['totalT'],None,datenow,None,py.pname,flask_login.current_user.id)
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
    obr = query(Obrero,flask_login.current_user.id)
    prv = query(Proveedor,flask_login.current_user.id)
    mt = query(Material,flask_login.current_user.id)
    deposito = flask_login.current_user.depo
    return render_template('gestionProy.html', data=proy, trps=trP, obrs=obr, prov=prv, mats=mt, depo=deposito)

@app.route('/pend/<name>/<proy>')
@login_required
def penScr(name,proy):
    trp = queryTP(TrabajoP,name,flask_login.current_user.id)
    p = queryP(Proyecto,proy,flask_login.current_user.id)
    obr = query(Obrero,flask_login.current_user.id)
    return render_template('pendiente.html', pr=p, tps=trp, obrs=obr)

@app.route('/pendC/<name>/<proy>')
@login_required
def asig(name, proy):
    #chequear materiales disponibles
    m = {}
    with store.open_session() as session:
        trp = list(  # Materialize query
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("tpname",name)
            .where_equals("Proyecto",proy)
            .where_equals("User", flask_login.current_user.id)# Filter
        )
        p = list(
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname", proy)
            .where_equals("User", flask_login.current_user.id)
        )

        usr = list(
            session
            .query(object_type=User)  # Query for Products
            .where_equals("id", flask_login.current_user.id)
        )

        for x in trp[0].matsNec:
            m[x['name']]=x['cant']
        pm = usr[0].depo
        err = []
        if pm:
            for key in pm.keys():
                #pm: disponibles, m: necesarios
                if key in m.keys():
                    if pm[key] < m[key]:
                        e = 'No hay suficiente '+key+'.'
                        err.append(e)

        if not err:
            for key in usr[0].depo.keys():
                if key in m.keys():
                    usr[0].depo[key]-=m[key]

            if not trp[0].matsDisp:
                trp[0].matsDisp = []
                for x in trp[0].matsNec:
                    trp[0].matsDisp.append(x)

            session.save_changes()
        else:
            return render_template('error.html', error=err)
    store.close()
    return redirect(url_for('deetsProy', name = p[0].pname))

@app.route('/comp/<name>/<proy>')
@login_required
def compTR(name, proy):
    err = []
    with store.open_session() as session:
        trp = list(  # Materialize query
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("tpname", name)
            .where_equals("Proyecto", proy)
            .where_equals("User", flask_login.current_user.id)  # Filter
        )
        p = list(
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname", proy)
            .where_equals("User", flask_login.current_user.id)
        )
        print(trp)
        print(p)
        if not trp[0].Obreros:
            e = 'No hay Obreros asignados.'
            err.append(e)
        if not err:
            trp[0].fechaFin = dateNow()
            p[0].compTR(trp[0])  # Hacer dict para que no guarde tan complejo
            session.delete_by_entity(trp[0])
            session.save_changes()
        else:
            return render_template('error.html', error=err)
    store.close()
    return redirect(url_for('deetsProy', name=p[0].pname))

@app.route('/addExtra/<name>', methods=["GET", "POST"])
@login_required
def addExtra(name):
    if request.method == 'POST':
        tpname = request.form['tp']
        mt = request.form['mat']
        matName = mt.split(' / ',1)[0]
        cant = request.form['cant']
        err = []
        with store.open_session() as session:
            trp = list(  # Materialize query
                session
                .query(object_type=TrabajoP)  # Query for Products
                .where_equals("tpname", tpname)
                .where_equals("Proyecto", name)
                .where_equals("User", flask_login.current_user.id)  # Filter
            )
            p = list(
                session
                .query(object_type=Proyecto)  # Query for Products
                .where_equals("pname", name)
                .where_equals("User", flask_login.current_user.id)
            )
            pm = p[0].MatsDisponibles
            if pm:
                for key in pm.keys():
                    # pm: disponibles, m: necesarios
                    if key == matName:
                        if pm[key] < int(cant):
                            e = 'No hay suficiente ' + key + '.'
                            err.append(e)
            if not err:
                p[0].MatsDisponibles[matName] -= int(cant)
                for x in trp[0].matsDisp:
                    if x['name'] == matName:
                        x['cant'] += int(cant)
            else:
                return render_template('error.html', error=err)
            session.save_changes()
        store.close()

        return redirect(url_for('deetsProy', name=p[0].pname))
@app.route('/assigOb/<job>/<name>/<py>')
@login_required
def addObr(job,name,py):
    p = queryP(Proyecto,py,flask_login.current_user.id)
    with store.open_session() as session:
        qObr = list(
            session
            .query(object_type=Obrero)  # Query for Products
            .where_equals("name", name)
            .where_equals("User", flask_login.current_user.id)
        )

        qTbs = list(
            session
            .query(object_type=TrabajoP)  # Query for Products
            .where_equals("tpname", job)
            .where_equals("User", flask_login.current_user.id)
        )
        qTbs[0].addObrero(qObr[0].name,qObr[0].occ, p.pname)
        qObr[0].addTrabajo(job,p.pname,dateNow())
        session.save_changes()
    store.close()
    return redirect(url_for('deetsProy', name = p.pname))



@login_manager.unauthorized_handler
def unauthorized():
    return render_template('login.html')

@app.route('/add_mat', methods=['POST'])
@login_required
def add_mats():
    if request.method == 'POST':
        name = request.form['mname']
        tipo = request.form['type']
        precio = request.form['price']
        x = request.form['source']
        prov = x.split(" / ",1)[0]
        x = queryN(Proveedor,prov,flask_login.current_user.id)
        #(self, name, type, price, Proveedor, cant)
        material = Material(name,tipo,precio, x,0,flask_login.current_user.id)
        addObject(material)
        return redirect(url_for('rmats'))

@app.route('/editScreen/<name>')
@login_required
def edit_mat(name):
    m = queryN(Material,name,flask_login.current_user.id)
    p = query(Proveedor,flask_login.current_user.id)
    return render_template('editMScreen.html', mat=m, provs=p)

@app.route('/edit_mat', methods=['POST'])
@login_required
def editS():
    if request.method == 'POST':
        name = request.form['mname']
        tipo = request.form['type']
        precio = int(request.form['price'])
        x = request.form['source']
        prov = x.split(" / ", 1)[0]
        x = queryN(Proveedor, prov,flask_login.current_user.id)
        newTM = 0
        # (self, name, type, price, Proveedor, cant)
        material = queryN(Material,name,flask_login.current_user.id)
        with store.open_session() as session:
            m = list(
                session
                .query(object_type=Material)  # Query for Products
                .where_equals("name", name)
                .where_equals("User", flask_login.current_user.id)
            )
            trb = list(
                session
                .query(object_type=Trabajo)
                .where_equals("User", flask_login.current_user.id)# Query for Products
                #.where_equals("name", name)
            )
            m[0].name=name
            m[0].type=tipo
            m[0].price=precio
            m[0].Proveedor=x
            for t in trb:
                for mt in t.Materiales:
                    if mt['name']==name:
                        mt['name'] = name
                        mt['type'] = tipo
                        mt['price'] = precio
                        mt['Proveedor'] = x
                        mt['total']=mt['price']*mt['cant']

            for tr in trb:
                for mt in t.Materiales:
                    newTM += mt['total']
                tr.totalM = newTM
                tr.total = tr.totalM+tr.priceM

            session.save_changes()

        store.close()
        t = datetime.datetime.now()
        newM = queryN(Material,name,flask_login.current_user.id)
        audit = Audit(material,newM,t, flask_login.current_user)
        addObject(audit)
        return redirect(url_for('rmats'))

@app.route('/verPagos/<name>')
@login_required
def pagos(name):
    p = queryP(Proyecto, name, flask_login.current_user.id)
    pagos = p.pagos
    pend = []
    for x in pagos:
        if x['Estado'] == 'Sin pagar':
            pend.append(x)
    return render_template('pagos.html', pagos=pagos, pr=p, pd=pend)

@app.route('/add_pay/<name>', methods=['POST'])
@login_required
def add_pay(name):
    p = queryP(Proyecto, name, flask_login.current_user.id)
    val = ''
    pago = 0
    f = {}
    if request.method == 'POST':
        cuota = request.form['cuota']

        with store.open_session() as session:
            data = list(
                session
                .query(object_type=Proyecto)  # Query for Products
                .where_equals("pname", name)

            )

            for x in data:
                if x.User == flask_login.current_user.id:
                    val = x

            for i in range(int(cuota)):
                val.pagos[i]['Estado'] = 'Pagado'
                pago += val.pagos[i]['MontoTotal']
                iva = val.pagos[i]['IVA']

            val.budget += pago

            cliente = val.Cliente
            f['Cliente'] = p.Cliente['name']
            f['RUC'] = p.Cliente['ruc']
            f['Detalles'] = 'Materiales y Mano de Obra'
            f['IVA'] = iva
            f['Cuotas'] = int(cuota)
            f['Valor'] = pago
            session.save_changes()
        store.close()
        return render_template('factura.html', factura=f, date=dateNow(), client=cliente, proy=val)

@app.route('/add_ped/<name>', methods=['POST'])
@login_required
def add_ped(name):
    p = queryP(Proyecto, name,flask_login.current_user.id)
    x = request.form['mat']
    mtname = x.split(' / ',1)[0]
    mat = queryN(Material,mtname,flask_login.current_user.id)
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
                .where_equals("User", flask_login.current_user.id)
            )
            usr = list(
                session
                .query(object_type=User)  # Query for Products
                .where_equals("id", flask_login.current_user.id)
            )

            if usr[0].depo:
                keys =  usr[0].depo.keys()
                if mat.name in keys:
                    usr[0].depo[mat.name]+=val
                else:
                    usr[0].depo[mat.name] = val
            else:
                m = {
                    mat.name: val
                }
                usr[0].depo = m
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
        p = Proveedor(name,email,tel,city,addr,flask_login.current_user.id)
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

        obr = Obrero(name, tel, occ, ced, cont, blood, addr, cont1, cont2, act, jobs, flask_login.current_user.id)
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

        pres = Presupuesto(obra, client, addr, jobs, status, budget,flask_login.current_user.id)
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

        client = Cliente(name,phone,addr,ruc,mail,city,type,flask_login.current_user.id)
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
            aux = queryN(Material, m, flask_login.current_user.id)
            #aux = q[0]
            #(self, name, type, price, Proveedor, cant)
            mat = Material(aux.getName(),aux.getType(),int(aux.getPrice()),'',int(c),flask_login.current_user.id)
            jmats.append(mat)
        total = 0
        for mat in jmats:
            total += int(mat.getTotal())


        trabajo = Trabajo(name,int(precio), total, (int(precio)+total) ,desc,jmats,0,flask_login.current_user.id)
        trabajo.medicion = md
        addObject(trabajo)
        return redirect(url_for('rjobs'))


@app.route('/details/<name>', methods=['GET','POST'])
@login_required
def deets(name):
    pres = queryPr(Presupuesto,name,flask_login.current_user.id)
    jobsL = pres.Trabajos

    return render_template('detalles.html', info=pres, listado=jobsL, fecha=dateNow())

@app.route('/add_pr/<pr>', methods=['POST','GET'])
@login_required
def add_pr(pr):
    if request.method == 'POST':
        ct = int(request.form['cant'])
        jbname = request.form['jb']
        j = queryN(Trabajo,jbname,flask_login.current_user.id)
        print(jbname,"  ",j.name)
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
            "totalT": (j.totalM * ct)+(j.priceM*ct),
            "desc": j.desc,
            "Materiales": mats,
            "Superficie": ct,
            "Medicion": j.medicion
        }
        with store.open_session() as session:
            data = list(
                session
                .query(object_type=Presupuesto)  # Query for Products
                .where_equals("oname", pr)
                .where_equals("User", flask_login.current_user.id)
            )
            val = ''
            for x in data:
                if x.User == flask_login.current_user.id:
                    val = x
            val.addJob(tb)
            val.addBudget(tb['totalT'])
            session.save_changes()
        store.close()

    return redirect('/cargaPres/'+pr)
    #return redirect('/cargaPres/' + pres[0].oname)
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
        data = list(  # Materialize query
            session
            .query(object_type=Presupuesto)  # Query for Products
            .where_equals("oname", pres)
            .where_equals("User", flask_login.current_user.id)# Filter
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )

        p = ''
        for x in data:
            if x.User == flask_login.current_user.id:
                p = x
        for t in p.Trabajos:
            if t['name'] == name:
                p.budget-=t['totalT']
                t.clear()
        tl = p.Trabajos
        newtl = list(filter(None,tl))
        p.Trabajos = newtl
        session.save_changes()

    store.close()

    return redirect(url_for('nbgt', name = pres))

@app.route('/del_job/<name>', methods=['POST','GET'])
@login_required
def del_job(name):
    job = ''
    with store.open_session() as session:
        p = list(  # Materialize query
            session
            .query(object_type=Trabajo)  # Query for Products
            .where_equals("name", name)
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        for x in p:
            if x.User == flask_login.current_user.id:
                job = x
        if job != '':
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
            .where_equals("name", name)
            .where_equals("User", flask_login.current_user.id)# Filter
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        session.delete_by_entity(p[0])
        session.save_changes()

    store.close()

    return redirect(url_for('rmats'))

@app.route('/delObr/<name>/<ced>', methods=['POST','GET'])
@login_required
def del_obr(name,ced):
    with store.open_session() as session:
        o = list(  # Materialize query
            session
            .query(object_type=Obrero)  # Query for Products
            .where_equals("name", name)
            .where_equals("ced", ced)
            .where_equals("User", flask_login.current_user.id)
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        #session.delete_by_entity(o[0])
        print(o)
        session.save_changes()
    store.close()

    return redirect('/pers')

@app.route('/delUsr/<id>', methods=['POST','GET'])
@login_required
def del_usr(id):
    with store.open_session() as session:
        u = list(  # Materialize query
            session
            .query(object_type=User)  # Query for Products
            .where_equals("id", id)
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        session.delete_by_entity(u[0])
        session.save_changes()
    store.close()

    return redirect('/pers')

@app.route('/baja', methods=['POST','GET'])
@login_required
def darBaja():
    if request.method == 'POST':
        x = request.form['obrero']
        obName = x.split(' / ',1)[0]
        obCed = x.split(' / ',1)[1]
        mot = request.form['baja']
        with store.open_session() as session:

            o = list(  # Materialize query
                session
                .query(object_type=Obrero)
                .where_equals("name",obName)# Query for Products
                .where_equals("ced", obCed)# Filter
                # .skip(0).take(10)                       # Page
                #.select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
            )
            o[0].isActive = 'No ('+mot+')'
            session.save_changes()
        store.close()

    return redirect('/pers')

@app.route('/alta/<name>/<ced>', methods=['POST','GET'])
@login_required
def darAlta(name,ced):
    with store.open_session() as session:
        o = list(  # Materialize query
            session
            .query(object_type=Obrero)
            .where_equals("name", name)  # Query for Products
            .where_equals("ced", ced)  # Filter
            # .skip(0).take(10)                       # Page
            # .select('oname', 'Cliente', "addr", 'Trabajos', 'status', 'budget')  # Project
        )
        o[0].isActive = 'Si'
        session.save_changes()
    store.close()
    return redirect('/pers')

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
    pres = Presupuesto('test',current_user,budget,flask_login.current_user.id)
    addObject(pres)
    return redirect('/home')

@app.route('/login')
def loginScreen():

    return flask.render_template('login.html')

@app.route('/signup')
def signup():
    err = []
    return flask.render_template('signup.html', form=data, error=err)

@app.route('/signup', methods=['GET', 'POST'])
def crearCuenta():
    if request.method == 'POST':
        err = []
        username = request.form['username']
        rname = request.form['realname']
        mail = request.form['mail']
        clave = request.form['pass']
        rclave = request.form['rpass']

        usr = queryID(User,username)

        if clave != rclave:
            err.append('Las contraseñas deben ser iguales.')
        if usr:
            err.append('Ya existe ese usuario.')

        if err:
            return flask.render_template('signup.html', error=err)
        else:
            usr = User(username,rname,mail,clave,None)
            addObject(usr)
            return flask.render_template('login.html')





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
            return redirect('/login')
        else:
            login_user(users[0])
            current_user = users[0]
            return flask.render_template('homescreen.html', form=data)





if __name__=="__main__":
        app.run(port=3000,debug=True)

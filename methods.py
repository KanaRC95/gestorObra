from pyravendb.store import document_store
from classes import *
import datetime
store = document_store.DocumentStore(urls=["http://localhost:8080"], database="gestorObra")
store.initialize()
import os
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice

def addObject(obj):
    with store.open_session() as session:
        session.store(obj)
        session.save_changes()
        store.close()

def query(type, user):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)
            .where_equals("User",user)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data

def queryID(type, id):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)
            .where_equals("id",id)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data

def queryN(type, name, user):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)  # Query for Products
            .where_equals("name",name)
            .where_equals("User",user)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data[0]

def queryTPr(type,proy):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)  # Query for Products
            .where_equals("Proyecto",proy)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data

def queryP(type, name, user):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)  # Query for Products
            .where_equals("pname",name)
            .where_equals("User",user)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data[0]

def queryTP(type, name, user):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)  # Query for Products
            .where_equals("tpname",name)
            .where_equals("User",user)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data[0]

def queryPr(type, name, user):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=type)  # Query for Products
            .where_equals("oname",name)
            .where_equals("User",user)  # Filter
            # .skip(0).take(10)                       # Page
            #.select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return data[0]

def queryMats():
    with store.open_session() as session:
        matList = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return matList

def queryMatsN(name):
    with store.open_session() as session:
        matList = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            .where_equals("name",name)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "unit", "contacto", "type","price", "Proveedor","cant")  # Project
        )
    store.close()
    return matList

def queryJobs():
    with store.open_session() as session:
        jobList = list(  # Materialize query
            session
            .query(object_type=Trabajo)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('name', 'priceM', 'totalM', 'totalT','desc', 'Materiales')  # Project
        )
    store.close()
    return jobList
def queryClients():
    with store.open_session() as session:
        clientList = list(  # Materialize query
            session
            .query(object_type=Cliente)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "phone", "addr", "ruc", "email", "ciudad","type")  # Project
        )
    store.close()
    return clientList

def queryPersonnel():
    with store.open_session() as session:
        clientList = list(  # Materialize query
            session
            .query(object_type=Obrero)  # Query for Products
            # .where_greater_than("UnitsInStock", 5)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('name', 'tel', 'occ', 'isCont', 'bloodT', 'addr', 'cont1', 'cont2', 'isActive', 'Trabajos')  # Project
        )
    store.close()
    return clientList

def queryClient(ruc):
    with store.open_session() as session:
        clientList = list(  # Materialize query
            session
            .query(object_type=Cliente)  # Query for Products
            .where_equals("ruc",ruc)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "phone", "addr", "ruc", "email", "ciudad","type")  # Project
        )
    store.close()
    return clientList[0]

def queryPres():
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=Presupuesto)  # Query for Products
            #.where_equals("name",name)  # Filter
            # .skip(0).take(10)                       # Page
            .select('oname', 'Cliente', 'Trabajos', 'status','budget')  # Project
        )
    store.close()
    return data

def queryProy():
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=Proyecto)  # Query for Products
            #.where_equals("name",name)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('pname', 'Cliente', 'addr', 'MatsFaltantes','MatsDisponibles', 'Obreros', 'Capataz', 'fechaInicio', 'fechaFin', 'Pedidos', 'TrabajosR', 'TrabajosD', 'presupuestado' ,'budget', 'status')  # Project
        )
    store.close()
    return data

def queryProyL(name):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=Proyecto)  # Query for Products
            .where_equals("pname",name)  # Filter
            # .skip(0).take(10)                       # Page
            .select('pname', 'Cliente', 'addr', 'MatsFaltantes','MatsDisponibles', 'Obreros', 'Capataz', 'fechaInicio', 'fechaFin', 'Pedidos', 'TrabajosR', 'TrabajosD', 'presupuestado' ,'budget', 'status')  # Project
        )
    store.close()
    if data:
        return data[0]
    else:
        return None

def queryPresL(oname):
    with store.open_session() as session:
        data = list(  # Materialize query
            session
            .query(object_type=Presupuesto)  # Query for Products
            .where_equals("oname",oname)  # Filter
            # .skip(0).take(10)                       # Page
            #.select('oname', 'Cliente', "addr" ,'Trabajos', 'status','budget')  # Project
        )
    store.close()
    return data

def queryJobsL(name):
    with store.open_session() as session:
        jobList = list(  # Materialize query
            session
            .query(object_type=Trabajo)  # Query for Products
            .where_equals("name",name)  # Filter
            # .skip(0).take(10)                       # Page
            .select('name', 'priceM', 'totalM', 'totalT','desc', 'Materiales')  # Project
        )
    store.close()
    return jobList

def mats ():
    temp =[]
    data = []
    mats = queryMats()
    for x in mats:
        temp.append(x.getName())
        temp.append(x.getType())
        temp.append(x.getPrice())
        data.append(temp)
        temp = []
    return(data)

def jobs ():
    temp =[]
    data = []
    trab = queryJobs()
    for x in trab:
        temp.append(x.getName())
        temp.append(x.priceM)
        temp.append(x.totalM)
        temp.append(x.totalT)
        temp.append(x.getDesc())
        temp.append(x.Materiales)
        temp.append(x.medicion)
        data.append(temp)
        temp = []
    return(data)

def matNames():
    r = []
    m = queryMats()
    for x in m:
        r.append(x.name)
    return r

def personnel():
    #name, tel, occ, isCont, bloodT, addr, cont1, cont2, isActive, Trabajos
    temp = []
    data = []
    pr = queryPersonnel()
    for x in pr:
        temp.append(x.name)
        temp.append(x.tel)
        temp.append(x.occ)
        temp.append(x.ced)
        temp.append(x.isCont)
        temp.append(x.bloodT)
        temp.append(x.addr)
        temp.append(x.cont1)
        temp.append(x.cont2)
        temp.append(x.isActive)
        temp.append(x.Trabajos)
        data.append(temp)
        temp = []
    return (data)

def clients ():
    temp =[]
    data = []
    cl = queryClients()
    for x in cl:
        temp.append(x.name)
        temp.append(x.phone)
        temp.append(x.addr)
        temp.append(x.ruc)
        temp.append(x.email)
        temp.append(x.ciudad)
        temp.append(x.type)
        data.append(temp)
        temp = []
    return(data)

def dateNow():
    return datetime.datetime.now().strftime("%x")

def pres():
    temp = []
    data = []
    pr = queryPres()
    for x in pr:
        temp.append(x.oname)
        temp.append(x.Cliente)
        temp.append(x.addr)
        temp.append(x.Trabajos)
        temp.append(x.status)
        temp.append(x.budget)
        data.append(temp)
        temp = []
    return(data)


def proyL():
    temp = []
    data = []
    pr = queryProy()
    # pname, Cliente, addr, Materiales, Obreros, Capataz, fechaInicio, fechaFin,
    # Pedidos, TrabajosR, TrabajosD, budget
    for x in pr:
        temp.append(x.pname)
        temp.append(x.Cliente)
        temp.append(x.addr)
        temp.append(x.MatsFaltantes)
        temp.append(x.MatsDisponibles)
        temp.append(x.fechaInicio)
        temp.append(x.budget)
        temp.append(x.status)
        data.append(temp)
        temp = []
    return(data)

def presL(oname):
    temp = []
    data = []
    pr = queryPresL(oname)
    for x in pr:
        temp.append(x.oname)
        temp.append(x.Cliente)
        temp.append(x.addr)
        temp.append(x.Trabajos)
        temp.append(x.status)
        temp.append(x.budget)
        data.append(temp)
        temp = []
    return(data[0])

def queryUsers(id,password):
    with store.open_session() as session:
        userList = list(  # Materialize query
            session
            .query(object_type=User)  # Query for Products
            .where_equals("id",id)
            .where_equals("password",password) # Filter
            # .skip(0).take(10)                       # Page
            #.select("id","name")  # Project
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

def invoice():
    os.environ["INVOICE_LANG"] = "es"
    client = Client('Client company')
    provider = Provider('STechies', bank_account='6454-6361-217273', bank_code='2021')
    creator = Creator('Karl Iris')
    invoice = Invoice(client, provider, creator)

    invoice.add_item(Item(1, 1000000, description="Materiales y Mano de Obra"))
    invoice.currency = "Gs."
    invoice.number = "10393069"
    docu = SimpleInvoice(invoice)
    docu.gen("templates/invoice2.pdf", generate_qr_code=False)  # you can put QR code by setting the #qr_code parameter to ‘True’

    # docu.gen("invoice.xml") ## We can also generate an XML file of this invoice
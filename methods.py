from pyravendb.store import document_store
from classes import *
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

def queryMatsN(name):
    with store.open_session() as session:
        matList = list(  # Materialize query
            session
            .query(object_type=Material)  # Query for Products
            .where_equals("name",name)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "unit", "contacto", "type","price", "proveedor")  # Project
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
            .select("name", "price", "desc")  # Project
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
            .select("name", "contacto")  # Project
        )
    store.close()
    return clientList

def queryJobsL(name):
    with store.open_session() as session:
        jobList = list(  # Materialize query
            session
            .query(object_type=Trabajo)  # Query for Products
            .where_equals("name",name)  # Filter
            # .skip(0).take(10)                       # Page
            .select("name", "price", "desc")  # Project
        )
    store.close()
    return jobList
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
    return(data)

def jobs ():
    temp =[]
    data = []
    mats = queryJobs()
    for x in mats:
        temp.append(x.getName())
        #x.setPrice()
        temp.append(x.getPrice())
        temp.append(x.getDesc())
        data.append(temp)
        temp = []
    return(data)

def clients ():
    temp =[]
    data = []
    cl = queryClients()
    for x in cl:
        temp.append(x.getName())
        temp.append(x.getCont())
        data.append(temp)
        temp = []
    return(data)

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
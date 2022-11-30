class User():
    def __init__(self, id, name, email, password, auth= True, active= True, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.auth = auth
        self.active = active
        self.is_admin = is_admin
    def is_authenticated(self):
        return self.auth
    def is_active(self):
        return self.active
    def get_id(self):
        return  self.id
    def __repr__(self):
        return '<User {}>'.format(self.email)

class Trabajo:

    def __init__(self,name, priceM, totalM, totalT, desc, Materiales):
        self.name = name
        self.priceM = priceM
        self.totalM = totalM
        self.desc = desc
        self.Materiales = Materiales
        self.totalT = totalT




    def getName(self):
        return self.name

    def getPrice(self):
        return self.priceM

    def getPrice(self):
        return self.priceM

    def getDesc(self):
        return self.desc

    def getMateriales(self):
        return self.Materiales




class Material:
    def __init__(self, name, type, price, Proveedor, cant):
        self.name = name
        self.type = type
        self.price = price
        self.Proveedor = Proveedor
        if cant == 0:
            self.total = 0
            self.cant = 0
        else:
            self.cant = cant
            self.total = int(self.price) * int(self.cant)


    def getName(self):
        return self.name

    def getType(self):
        return self.type

    def getSource(self):
        return self.Proveedor

    def getPrice(self):
        return self.price

    def setTotal(self):
        self.total = int(self.price) * int(self.cant)
        return self.total

    def getTotal(self):
        return self.total



class Proveedor():
    def __init__(self,nombre, email, cel, city):
        self.nombre = nombre
        self.email = email
        self.cel = cel
        self.city = city

    def getName(self):
        return self.nombre
    def getMail(self):
        return self.email
    def getCel(self):
        return self.cel
    def getCity(self):
        return self.city

class Cliente():
    def __init__(self,name, phone, addr, ruc, email, ciudad, type):
        self.name = name
        self.phone = phone
        self.addr = addr
        self.ruc = ruc
        self.email = email
        self.ciudad = ciudad
        self.type = type

    def getName(self):
        return self.name

    def getCont(self):
        return self.contacto

class Obrero():
    def __init__(self,name, tel, occ, isCont, bloodT, addr, cont1, cont2, isActive, Trabajos):
        self.name = name
        self.tel = tel
        self.occ = occ
        self.isCont = isCont
        self.bloodT = bloodT
        self.addr = addr
        self.cont1 = cont1
        self.cont2 = cont2
        self.isActive = isActive
        self.Trabajos = Trabajos

class Proyecto():
    def __init__(self, pname, Cliente, addr, Materiales, Obreros, Capataz, fechaInicio, fechaFin,
                 Pedidos, TrabajosR, TrabajosD, budget):

        self.pname = pname
        self.Cliente = Cliente
        self.addr = addr
        self.Materiales = Materiales
        self.Obreros = Obreros
        self.Capataz = Capataz
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.Pedidos = Pedidos
        self.TrabajosR = TrabajosR
        self.TrabajosD = TrabajosD
        self.budget = budget

class Presupuesto():
    def __init__(self,oname, Cliente, addr, Trabajos, status, budget):
        self.oname = oname
        self.Cliente = Cliente
        self.addr = addr
        self.Trabajos = Trabajos
        self.status = status
        self.budget = budget

    def addJob(self,job):
        if not self.Trabajos:
            jobs = []
            jobs.append(job)
            self.Trabajos = jobs
        else:
            self.Trabajos.append(job)

    def getJobs(self):
        return self.Trabajos

    def addBudget(self,val):
        self.budget += int(val)

    def getBudget(self):
        return self.budget

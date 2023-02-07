class User():
    def __init__(self, id, name, email,password, depo, auth= True, active= True, is_admin=False):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.auth = auth
        self.depo = depo
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
    def __init__(self,name, priceM, totalM, totalT, desc, Materiales, medicion, User):
        self.name = name
        self.priceM = priceM
        self.totalM = totalM
        self.desc = desc
        self.Materiales = Materiales
        self.totalT = totalT
        self.superficie = 0
        self.medicion = medicion
        self.User = User

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


class TrabajoP:
    def __init__(self, tpname, matsNec, matsDisp, precioTotal, Obreros, fechaInicio, fechaFin, Proyecto, User):
        self.tpname = tpname
        self.matsNec = matsNec
        self.matsDisp = matsDisp
        self.precioTotal = precioTotal
        self.Obreros = Obreros
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.Proyecto = Proyecto
        self.User = User


    def addObrero(self,name, occ, proy):
        if not self.Obreros:
            obs = []
            ob = {
                "Nombre": name,
                "Ocupacion": occ,
                "Proyecto": proy
            }
            obs.append(ob)
            self.Obreros = obs
        else:
            ob = {
                "Nombre": name,
                "Ocupacion": occ,
                "Proyecto": proy
            }
            self.Obreros.append(ob)

class Material:
    def __init__(self, name, type, price, Proveedor, cant, User):
        self.name = name
        self.type = type
        self.price = price
        self.Proveedor = Proveedor
        self.User = User
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
    def __init__(self,name, email, cel, city, addr, User):
        self.name = name
        self.email = email
        self.cel = cel
        self.city = city
        self.addr = addr
        self.User = User

    def getName(self):
        return self.name
    def getMail(self):
        return self.email
    def getCel(self):
        return self.cel
    def getCity(self):
        return self.city

class Cliente():
    def __init__(self,name, phone, addr, ruc, email, ciudad, type, User):
        self.name = name
        self.phone = phone
        self.addr = addr
        self.ruc = ruc
        self.email = email
        self.ciudad = ciudad
        self.type = type
        self.User = User

    def getName(self):
        return self.name

    def getCont(self):
        return self.contacto

class Obrero():
    def __init__(self,name, tel, occ, ced, isCont, bloodT, addr, cont1, cont2, isActive, Trabajos, User):
        self.name = name
        self.tel = tel
        self.occ = occ
        self.ced = ced
        self.isCont = isCont
        self.bloodT = bloodT
        self.addr = addr
        self.cont1 = cont1
        self.cont2 = cont2
        self.isActive = isActive
        self.Trabajos = Trabajos
        self.User = User

    def addTrabajo(self,job, Proy, date):
        if not self.Trabajos:
            jobs = []
            jb = {
                "Trabajo": job,
                "Proyecto": Proy,
                "Fecha: ": date
            }
            jobs.append(jb)
            self.Trabajos = jobs
        else:
            jb = {
                "Trabajo": job,
                "Proyecto": Proy,
                "Fecha: ": date
            }
            self.Trabajos.append(jb)




class Proyecto():
    def __init__(self, pname, Cliente, addr, MatsFaltantes, MatsDisponibles, Obreros, Capataz, fechaInicio, fechaFin,
                 Pedidos, TrabajosR, TrabajosD, presupuestado, budget, status, pagos, gastos, User):

        self.pname = pname
        self.Cliente = Cliente
        self.addr = addr
        self.MatsFaltantes = MatsFaltantes
        self.MatsDisponibles = MatsDisponibles
        self.Obreros = Obreros
        self.Capataz = Capataz
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin
        self.Pedidos = Pedidos
        self.TrabajosR = TrabajosR
        self.TrabajosD = TrabajosD
        self.presupuestado = presupuestado
        self.budget = budget
        self.status = status
        self.pagos = pagos
        self.gastos = gastos
        self.User = User

    def movTR(self,elem):
        self.TrabajosR.remove(elem)

    def compTR(self, tr):
        if not self.TrabajosD:
            tc = []
            tc.append(tr)
            self.TrabajosD = tc
        else:
            self.TrabajosD.append(tr)

    def addFactura(self,f):
        if not self.pagos:
            pg = []
            pg.append(f)
            self.pagos = pg
        else:
            self.pagos.append(f)

class Presupuesto():
    def __init__(self,oname, Cliente, addr, Trabajos, status, budget, User):
        self.oname = oname
        self.Cliente = Cliente
        self.addr = addr
        self.Trabajos = Trabajos
        self.status = status
        self.budget = budget
        self.User = User

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

class Audit():
    def __init__(self, antes, despues, fecha, User):
        self.antes = antes
        self.despues = despues
        self.fecha = fecha
        self.User = User

class Pedido():
    def __init__(self,Material, fecha, Proyecto, User):
        self.Material = Material
        self.fecha = fecha
        self.Proyecto = Proyecto
        self.User = User

class Baja():
    def __init__(self, Material, cant, razon, fecha, User):
        self.Material = Material
        self.cant = cant
        self.razon = razon
        self.fecha = fecha
        self.User = User

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
    mats = []
    def __init__(self,name, price, desc, Materiales):
        self.name = name
        self.price = price
        self.desc = desc
        self.Materiales = Materiales


    def getName(self):
        return self.name
    def getPrice(self):
        price = 0
        if not self.Materiales:
            return price
        else:
            for mat in self.Materiales:
                price = price + int(mat.getPrice())
            return price
    def getDesc(self):
        return self.desc
    def getMateriales(self):
        return self.Materiales
    def addMaterial(self,obj):
        self.mats.append(obj)
        self.Materiales = self.mats
    def setPrice(self):
        price = 0
        for mat in self.Materiales:
            price = price + int(mat.getPrice())
        self.price = price
class Material:
    def __init__(self, name, unit, type, price, proveedor, contacto, User):
        self.name = name
        self.unit = unit
        self.type = type
        self.price = price
        self.proveedor = proveedor
        self.contacto = contacto
        self.user = User


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

    def getUser(self):
        return self.user

class Cliente():
    def __init__(self,name, contacto):
        self.name = name
        self.contacto = contacto

    def getName(self):
        return self.name

    def getCont(self):
        return self.contacto

class Obrero():
    def __init__(self,name):
        self.name = name

class Presupuesto():
    def __init__(self,cname, user, details):
        self.cname = cname
        self.user = user
        self.details = details


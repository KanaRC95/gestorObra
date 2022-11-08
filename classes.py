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
    def __init__(self,name, price, desc, User):
        self.name = name
        self.price = price
        self.desc = desc
        self.user = User


    def getName(self):
        return self.name
    def getPrice(self):
        return self.price
    def getDesc(self):
        return self.desc
    def getUser(self):
        return self.user

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


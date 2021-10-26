
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column , Integer ,DateTime
db = SQLAlchemy()

class marcas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(80) , nullable=False)
    items_marcas = db.relationship("Item")
    

class Item(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer , nullable=False)
    numeroOriginal = db.Column(db.Integer ,nullable=False)
    marca = db.Column(db.ForeignKey("marcas.id"))
    modelo = db.Column(db.String(80) , nullable=False)
    tipoCable = db.Column(db.String(80) , nullable=False)
    descripcion=db.Column(db.String(512))
    imagen_link =db.Column(db.String(128))
    consultados = db.relationship("Consultas")

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer , primary_key=True)
    Username=db.Column(db.String(50),nullable=False , unique=True)
    Password = db.Column(db.String(50), nullable=False)


class Consultas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_consultado = db.Column(db.ForeignKey("item.id"))
    nombre =db.Column(db.String(20))
    apellido =db.Column(db.String(20))
    telefono =db.Column(db.String(20))
    consulta = db.Column(db.String(512))
    visto = db.Column(db.Boolean , default = False)
    fecha = db.Column(DateTime , default=datetime.now) 




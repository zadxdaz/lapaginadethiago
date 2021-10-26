
from enum import unique
from itertools import product
from operator import is_not
from flask import Flask,render_template , request ,redirect , url_for
from flask.sessions import NullSession
from flask_login import login_manager
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from forms import Item_add , LoginForm, RegisterForm ,CatalogFilter , product_consulta
from flask_bootstrap import Bootstrap
from flask_login import LoginManager , UserMixin , login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
from database import db , Item , Users , marcas , Consultas

conector=sqlite3.connect("test.db")

app = Flask(__name__, static_url_path='/static')
Bootstrap(app)
app.config['SECRET_KEY'] = "\x05\r\xfdj>BT\x16i\\2|4;\x16\x0cz\xa9\xe86\xc2\xfd\xc9\xf2\x8f"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

#db.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.filter_by(id=id).first()


with app.app_context():
    db.init_app(app)
    db.create_all()


def json_table(items):
    list=[]
    marca=marcas.query
    for item in items:
        nombreMarca=marca[int(item.marca)-1].marca
        list.append({
            "codigo" : item.codigo ,
            "numeroOriginal" : item.numeroOriginal,
            "marca" : nombreMarca ,
            "modelo" : item.modelo , 
            "tipoDeCable" : item.tipoCable ,
            "descripcion" : item.descripcion , 
            "imagen_link" : item.imagen_link
        })
    return list

def json_producto(codigo):
    item=Item.query.filter_by(codigo=codigo).first()
    marca=marcas.query
    nombreMarca=marca[int(item.marca)-1].marca
    producto = {    
            "codigo" : item.codigo ,
            "numeroOriginal" : item.numeroOriginal,
            "marca" : nombreMarca ,
            "modelo" : item.modelo , 
            "tipoCable" : item.tipoCable ,
            "descripcion" : item.descripcion,
            "imagen_link" : item.imagen_link
        }
    return producto

def json_consultas(table):
    lista=[]
    items = Item.query
    for x in table:
        lista.append({
            "nombre" : x.nombre,
            "apellido" : x.apellido,
            "telefono" : x.telefono,
            "consulta" : x.consulta,
            "item_codigo" : items[int(x.producto_consultado)].codigo,
            "item_id" : x.producto_consultado
        })
    return lista
        



@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/add_producto" , methods=["GET","POST"])
@login_required
def add_producto():
    form=Item_add()
    
    if form.validate_on_submit():
        filename=form.codigo.data +".jpg"
        link="\static\photos/" + form.codigo.data + ".jpg"
        item=Item(codigo=form.codigo.data,numeroOriginal=form.numeroOriginal.data,
        marca=form.marca.data.id ,modelo=form.modelo.data,tipoCable=form.tipoCable.data,
        descripcion=form.descripcion.data,imagen_link=link)
        photo= form.imagen.data
        photo.save(os.path.join(
            os.path.dirname(app.instance_path),"static/photos",filename
        ))
        db.session.add(item)
        db.session.commit()
        return redirect("/add_producto")
    return render_template("add_item.html", form=form)

@app.route("/productos" , methods=["GET","POST"])
@login_required
def productos():
    try: 
        productos=json_table()
        return render_template("productos.html" , productos=productos )
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route("/eliminar/producto/<int:id>")
@login_required
def delete(id):
    try:
        Item.query.filter_by(codigo=id).delete()
        db.session.commit()
        return redirect("/productos")
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route("/login",methods=["GET","POST"] )
def login():
    if current_user.is_authenticated :
        return redirect("/dashboard")
    form=LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(Username=form.Username.data).first()
        if user:
            bcrypt.check_password_hash(user.Password ,form.Password.data)
            login_user(user)
            return redirect ("/dashboard")
    return render_template("login.html" ,form=form)

@app.route("/register" ,methods=["GET","POST"])
def register():
    form=RegisterForm()

    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.Password.data)
        user=Users(Username=form.Username.data,Password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html",form=form)

@app.route("/dashboard")
@login_required
def dashboard():
    consultas = json_consultas(
        Consultas.query.filter_by(visto=False)
    )
    return render_template("/dashboard.html" , consultas=consultas)

@app.route("/catalog" ,methods=["GET","POST"])
def catalog(marcaNombre=False):
    form = CatalogFilter()
    productos=json_table(Item.query)
    try: 
        if form.validate_on_submit():
            #codigo=str(form.codigo.data)
            #numeroOriginal=str(form.numeroOriginal.data)
            if form.marca.data is not None:
                productos=json_table(Item.query.filter_by(marca=form.marca.data.id))
                return render_template("catalog.html" , productos=productos, form=form)
            if form.codigo.data != "":
                productos=json_table(Item.query.filter_by(codigo=form.codigo.data))
                return render_template("catalog.html" , productos=productos, form=form)
            if form.numeroOriginal.data != "":
                productos=json_table(Item.query.filter_by(numeroOriginal=form.numeroOriginal.data))
                return render_template("catalog.html" , productos=productos, form=form)
        return render_template("catalog.html" , productos=productos, form=form)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route("/producto/<int:producto>" , methods=["GET","POST"])
def producto(producto):
    form = product_consulta()
    info = json_producto(producto)
    if form.validate_on_submit() :
        consulta = Consultas(
            nombre =form.nombre.data,
            apellido = form.apellido.data,
            telefono = form.telefono.data,
            consulta = form.consulta.data, 
            producto_consultado = producto
        )
        db.session.add(consulta)
        db.session.commit()
        return redirect("/catalogo")
    return render_template("producto.html" , info=info, form=form)


if __name__ == "__main__":
    app.run(debug=True)
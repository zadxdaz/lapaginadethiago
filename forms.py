
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, InputRequired, Length, ValidationError
from wtforms.widgets.core import TextArea
from flask_wtf.file import FileField
from database import db , Users , marcas
from wtforms_sqlalchemy.fields  import QuerySelectField

def validate_username(form,field):
    existing_user_name = Users.query.filter_by(Username=field.data).first()
    if existing_user_name:
            raise ValidationError("Ese nombre ya existe")
def marcas_a_elegir():
    return marcas.query
class Item_add(FlaskForm):
    codigo = StringField("Codigo de la Empresa",validators=[InputRequired()])
    numeroOriginal = StringField("Numero Original",validators=[InputRequired()])
    marca = QuerySelectField(query_factory=marcas_a_elegir , get_label="marca", allow_blank=False)
    modelo = StringField("Modelo",validators=[InputRequired()])
    tipoCable= StringField("Tipo de Cable",validators=[InputRequired()])
    descripcion=StringField("Descripcion")
    imagen = FileField("Imagen")
    submit= SubmitField("Agregar")    
class LoginForm(FlaskForm):
    Username = StringField("Usuario",validators=[InputRequired(), Length(min=6 , max=20)] )
    Password = PasswordField("Contraseña" ,validators=[InputRequired() , Length(min=6 , max=20)])
    submit= SubmitField("Ingresar")

class RegisterForm(FlaskForm):
    Username = StringField("Usuario",validators=[InputRequired(), Length(min=6 , max=20),validate_username] )
    Password = PasswordField("Contraseña" ,validators=[InputRequired() , Length(min=6 , max=20)])
    submit= SubmitField("Ingresar")

class CatalogFilter(FlaskForm):
    codigo = StringField("Codigo de la Empresa: ")
    numeroOriginal = StringField("Numero Original: ")
    marca = QuerySelectField("marca: ",query_factory=marcas_a_elegir , get_label="marca", allow_blank=True)
    submit= SubmitField("Submit")

class product_consulta(FlaskForm):
    nombre =StringField("Nombre: ")
    apellido = StringField("Apellido: ")
    telefono = StringField("Telefono :")
    consulta = StringField("Consulta: ")
    submit= SubmitField("Enviar Consulta")



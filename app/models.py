from app import db

class Company(db.Model):
    __tablename__ = 'Company'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    base_png = db.Column(db.String(120), index=True, unique=True)
    qr_x = db.Column(db.Integer)
    qr_y = db.Column(db.Integer)

class User(db.Model):
    __tablename__ = 'DC_Usuarios'
    correo = db.Column(db.String(120), primary_key=True)
    nombres = db.Column(db.String)
    apellidos =db.Column(db.String)
    extension = db.Column(db.Integer)
    celular = db.Column(db.String)
    puesto = db.Column(db.String(128))
    pagina_web = db.Column(db.String(128))
    ciudad = db.Column(db.String(64))
    pais = db.Column(db.String(64))
    departamento = db.Column(db.String(64))
    area= db.Column(db.String(64))
    codigo_postal = db.Column(db.String(64))
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'))

class Field(db.Model):
    __tablename__ = 'Field'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

class Detail(db.Model):
    __tablename__ = 'Detail'

    id_auto = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    red = db.Column(db.Integer)
    green = db.Column(db.Integer)
    blue = db.Column(db.Integer)
    position_x = db.Column(db.Integer)
    position_y = db.Column(db.Integer)
    font = db.Column(db.String(64))
    size_font = db.Column(db.Integer)
    is_center = db.Column(db.String(10))

    id_field = db.Column(db.Integer, db.ForeignKey('field.id'))
    id_company = db.Column(db.Integer, db.ForeignKey('company.id'))

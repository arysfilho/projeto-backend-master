from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    colaboradores = db.relationship('Colaborador', backref='departamento', lazy=True)

class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tem_dependentes = db.Column(db.Boolean, default=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'),nullable=False)
    dependentes = db.relationship('Dependente', backref='colaborador', lazy=True)

class Dependente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'),nullable=False)

db.create_all()
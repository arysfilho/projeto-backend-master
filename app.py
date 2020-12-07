from flask import Flask, request, jsonify
from sqlalchemy.exc import IntegrityError
from database.db import db, initialize_db, ma, initialize_ma
from database.models import Departamento, DepartamentoSchema, Colaborador, ColaboradorSchema, Dependente, DependenteSchema
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
initialize_db(app)
initialize_ma(app)

# Init schemas
departamento_schema = DepartamentoSchema()
departamentos_schema = DepartamentoSchema(many=True)
colaborador_schema = ColaboradorSchema()
colaboradores_schema = ColaboradorSchema(many=True)
dependentes_schema = DependenteSchema(many=True)

@app.route('/departamentos')
def get_departamentos():
    departamentos = Departamento.query.all()
    result = departamentos_schema.dump(departamentos)
    return jsonify(result), 200

@app.route('/departamentos', methods=['POST'])
def add_departamento():
    name = request.json['name']
    novo_departamento = Departamento(name)

    db.session.add(novo_departamento)
    db.session.commit()

    return departamento_schema.jsonify(novo_departamento), 201

@app.route('/departamentos/<id>', methods=['PUT'])
def update_departamento(id):
    name = request.json['name']
    try:
        departamento = Departamento.query.get(id)
    except IntegrityError:
        return {"message": "Departamento não encontrado."}, 400
    departamento.name = name
    db.session.commit()
    return '', 200

@app.route("/departamentos/<int:id>")
def get_departamento(id):
    try:
        departamento = Departamento.query.get(id)
    except IntegrityError:
        return {"message": "Departamento não encontrado."}, 400
    departamento_result = departamento_schema.dump(departamento)
    colaboradores_result = colaboradores_schema.dump(Colaborador.query.filter(Colaborador.departamento_id == id))
    return {"departamento": departamento_result, "colaboradores": colaboradores_result}

@app.route('/colaboradores')
def get_colaboradores():
    colaboradores = Colaborador.query.all()
    result = colaboradores_schema.dump(colaboradores)
    return jsonify(result), 200

@app.route('/colaboradores', methods=['POST'])
def add_colaborador():
    name = request.json['name']
    departamento_id = request.json['departamento_id']
    tem_dependentes = 'dependentes' in request.json
    novo_colaborador = Colaborador(name, departamento_id, tem_dependentes)

    db.session.add(novo_colaborador)
    db.session.commit()

    if 'dependentes' in request.json:
        for dep in request.json['dependentes']:
            novo_dependente = Dependente(dep, novo_colaborador.id)
            db.session.add(novo_dependente)
            db.session.commit()

    return departamento_schema.jsonify(novo_colaborador), 201

@app.route('/dependentes')
def get_dependentes():
    dependentes = Dependente.query.all()
    result = dependentes_schema.dump(dependentes)
    return jsonify(result), 200


app.run(debug=True)

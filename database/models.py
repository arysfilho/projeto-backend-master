from .db import db, ma

class Departamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

class Colaborador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    tem_dependentes = db.Column(db.Boolean, default=False)
    departamento_id = db.Column(db.Integer, db.ForeignKey('departamento.id'),nullable=False)
    departamento = db.relationship('Departamento', backref=db.backref("colaboradores", lazy="dynamic"))

    def __init__(self, name, departamento_id, tem_dependentes):
        self.name = name
        self.departamento_id = departamento_id
        self.tem_dependentes = tem_dependentes

class Dependente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    colaborador_id = db.Column(db.Integer, db.ForeignKey('colaborador.id'),nullable=False)
    colaborador = db.relationship('Colaborador', backref=db.backref("dependentes", lazy="dynamic"))

    def __init__(self, name, colaborador_id):
        self.name = name
        self.colaborador_id = colaborador_id

class DepartamentoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

class ColaboradorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'departamento_id', 'tem_dependentes')

class DependenteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'colaborador_id')
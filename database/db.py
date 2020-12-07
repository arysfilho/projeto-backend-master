from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Iniciar db
db = SQLAlchemy()

# Iniciar marshmallow
ma = Marshmallow()

def initialize_db(app):
    db.init_app(app)

def initialize_ma(app):
    ma.init_app(app)
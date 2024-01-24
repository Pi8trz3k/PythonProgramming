from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

def add_row(entity):
    db.session.add(entity)
    db.session.commit()

def get_row(entity, entity_id):
    row = db.session.get(entity, entity_id)
    db.session.commit()
    return row

def delete_row(entity):
    db.session.delete(entity)
    db.session.commit()

def get_all(entity):
    all_rows = db.session.query(entity).all()
    return all_rows

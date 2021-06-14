  
from datetime import datetime
from mainapp import db ,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), unique=True, nullable=False)
    prenom = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    niveau = db.Column(db.String(120), nullable=False)
    specialite = db.Column(db.String(120),  nullable=False)
    role = db.Column(db.String(120),  nullable=False)
    notes = db.relationship('Note', backref='Note_User',lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.nom}',{self.prenom}', '{self.email}','{self.niveau}','{self.specialite}','{self.role}')"

class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(40) ,nullable=False)    
    semestre = db.Column(db.Integer,nullable=False)
    niveau = db.Column(db.String(40),nullable=False)
    specialite = db.Column(db.String(40),nullable=False)
    module = db.Column(db.String(40),nullable=False)
    coefficient = db.Column(db.Float,nullable=False)
    notes = db.relationship('Note', backref='Note_Matiere',lazy=True)

    def __repr__(self):
        return f"matiere('{self.id}','{self.nom}','{self.semestre}','{self.niveau}','{self.specialite}','{self.module}','{self.coefficient}')"


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Float,nullable=False)
    nature = db.Column(db.String(20),nullable=False)   
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'),nullable=False)    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)    

    def __repr__(self):
        return f"note('{self.id}','{self.note}','{self.nature}','{self.matiere_id}','{self.user_id}')"


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10))
    # Relations
    relations = db.relationship('RelationContactGroup', backref='contact') #, foreign_keys='contact')

    def __repr__(self):
        return f'Contact {self.full_name} / {self.email}'

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "address": self.address,
            "phone": self.phone,
            "groups": list(map(lambda relation: relation.group.name, self.relations))
        }

class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Relations
    relations = db.relationship('RelationContactGroup', backref='group') #, foreign_keys='group')

    def __repr__(self):
        return f'Group {self.id} / {self.name}'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "contacts": list(map(lambda relation: relation.contact.serialize(), self.relations))
        }

class RelationContactGroup(db.Model):
    __tablename__ = 'relation_contact_group'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
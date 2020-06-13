from app import db
from dataclasses import dataclass


class Text(db.Model):

    __tablename__ = 'texts'
    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True,
                   nullable=False)
    name = db.Column(db.String(256))
    text_lines = db.relationship('TextLine', backref='Text', lazy=True)

    def __init__(self, id, name, text_lines):
        self.id = id
        self.name = name
        self.text_lines = text_lines

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialized(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TextLine(db.Model):

    __tablename__ = 'text_lines'
    id = db.Column(db.Integer,
                   primary_key=True,
                   unique=True,
                   nullable=False)
    line = db.Column(db.Text)
    text_id = db.Column(db.Integer,
                        db.ForeignKey('texts.id'),
                        nullable=False)

    def __init__(self, id, line, text_id):
        self.id = id
        self.line = line
        self.text_id = text_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @property
    def serialized(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

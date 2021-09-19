from database import db
from sqlalchemy.dialects import postgresql


class TicketModel(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(1000), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    intents = db.Column(postgresql.ARRAY(db.String))


class MessageModel(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    created = db.Column(db.String(1000), nullable=False)
    updated = db.Column(db.String(1000), nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    ticket_id = db.Column(db.Integer, nullable=False)
    incoming = db.Column(db.Boolean, nullable=False)

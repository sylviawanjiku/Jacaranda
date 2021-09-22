from marsh import ma
from database import db

from models import MessageModel,TicketModel
from marshmallow import fields


class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MessageModel
        include_relationships = True
        load_instance = True

messageListSchema = MessageSchema(many=True)

class TicketSchema(ma.SQLAlchemyAutoSchema):
  incoming_messages = fields.Method('get_incoming_messages')
  outgoing_messages = fields.Method('get_outgoing_messages')

  def get_incoming_messages(self, obj):
    messageListSchema = MessageSchema(many=True)
    msgs = db.session.query(MessageModel).filter(
        MessageModel.ticket_id==obj.ticket_id, MessageModel.incoming==True)
    return messageListSchema.dump(msgs)
  
  def get_outgoing_messages(self, obj):
    messageListSchema = MessageSchema(many=True)
    msgs = db.session.query(MessageModel).filter(
        MessageModel.ticket_id == obj.ticket_id, MessageModel.incoming == False)
    return messageListSchema.dump(msgs)
  
  class Meta:
    model = TicketModel
    include_relationships = True
    load_instance = True
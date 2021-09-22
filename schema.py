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
    messages = db.session.query(MessageModel).filter(
        MessageModel.ticket_id==obj.ticket_id, MessageModel.incoming==True)
    return messageListSchema.dump(messages)
  
  def get_outgoing_messages(self, obj):
    messageListSchema = MessageSchema(many=True)
    messages = db.session.query(MessageModel).filter(
        MessageModel.ticket_id == obj.ticket_id, MessageModel.incoming == False)
    return messageListSchema.dump(messages)
  
  class Meta:
    model = TicketModel
    include_relationships = True
    load_instance = True
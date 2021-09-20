
from message import Message, MessageDetail
from ticket import Ticket, TicketDetail,LoadData
from flask import Flask
from flask_restful import Api
from database import db


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sly:@127.0.0.1/jacadb'


@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(LoadData,'/load-data/')
api.add_resource(Message, "/message/")
api.add_resource(MessageDetail, "/message/<int:message_id>")
api.add_resource(Ticket, "/ticket/")
api.add_resource(TicketDetail, "/ticket/<int:ticket_id>")


if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)

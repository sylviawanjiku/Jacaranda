import os
from message import Message, MessageDetail
from ticket import Ticket, TicketDetail,LoadData
from flask import Flask
from flask_restful import Api
from database import db
from config import app_config

""" create_app function wraps the creation and return of Flaskobject """  
def create_app(config_name):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    @app.before_first_request
    def create_tables():
        db.create_all()

    api.add_resource(LoadData,'/load-data/')
    api.add_resource(Message, "/message/")
    api.add_resource(MessageDetail, "/message/<int:message_id>")
    api.add_resource(Ticket, "/ticket/")
    api.add_resource(TicketDetail, "/ticket/<int:ticket_id>")

    return app

app = create_app(os.getenv('FLASK_ENV'))

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)

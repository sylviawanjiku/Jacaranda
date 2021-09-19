import pdb
from typing import List
from models import TicketModel
from flask_restful import Resource, reqparse, fields, marshal_with, inputs
from database import db
from schema import TicketSchema

tktSchema = TicketSchema()
tktListSchema = TicketSchema(many=True)

ticket_post_args = reqparse.RequestParser()
ticket_post_args.add_argument(
    "ticket_id", type=int, help="ticket_id is required", required=True)
ticket_post_args.add_argument(
    "subject", type=str, help="Subject is required", required=True)
ticket_post_args.add_argument(
    "phone", type=int, help="PhoneNumber is required", required=True)
ticket_post_args.add_argument(
    "intents", type=list, help="Intents are required", required=True)


ticket_patch_args = reqparse.RequestParser()
ticket_patch_args.add_argument(
    "ticket_id", type=int, help="ticket_id is required", required=False)
ticket_patch_args.add_argument(
    "subject", type=str, help="Subject is required", required=False)
ticket_patch_args.add_argument(
    "phone", type=int, help="PhoneNumber is required", required=False)
ticket_patch_args.add_argument(
    "intents", type=str, help="Intents are required", required=False)


resource_fields = {
    'ticket_id': fields.Integer,
    'subject': fields.String,
    'phone': fields.Integer,
    'intents':fields.List
}
TCKT_NOT_FOUND = "Ticket not found for id: {}"
TCKT_DELETE_SUCCESS = "Ticket deleted successfully for id: {}"


class TicketDetail(Resource):
    def get(self, ticket_id):
        result = TicketModel.query.filter_by(ticket_id=ticket_id).first()
        if result:
            return tktSchema.dump(result)
        return {'message': TCKT_NOT_FOUND.format(ticket_id)}, 404

    @marshal_with(resource_fields)
    def patch(self, ticket_id):
        tckt_req_json = ticket_patch_args.parse_args()
        tckt_data = TicketModel.query.filter_by(ticket_id=ticket_id).first()
        if tckt_data:
            if tckt_req_json.get('ticket_id', None):
                tckt_data.ticket_id = tckt_req_json['ticket_id']
            if tckt_req_json.get('subject', None):
                tckt_data.subject = tckt_req_json['subject']
            if tckt_req_json.get('phone', None):
                tckt_data.phone = tckt_req_json['phone']
            if tckt_req_json.get('intents', None):
                tckt_data.intents = tckt_req_json['intents']
            db.session.commit()
            return tktSchema.dump(tckt_data)
        return {'message': TCKT_NOT_FOUND.format(ticket_id)}, 404

    def delete(self, ticket_id):
        ticket = TicketModel.query.filter_by(ticket_id=ticket_id).delete()
        if ticket:
            db.session.commit()
            return {'message': TCKT_DELETE_SUCCESS.format(ticket_id)}, 200
        return {'message': TCKT_NOT_FOUND.format(ticket_id)}, 404


class Ticket(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = ticket_post_args.parse_args()
        import pdb; pdb.set_trace()
        ticket = TicketModel(
            ticket_id=args['ticket_id'],
            subject=args['subject'],
            phone=args['phone'],
            intents=args['intents']
        )
        db.session.add(ticket)
        db.session.commit()
        return ticket, 201

    def get(self):
        ticket = TicketModel.query.all()
        return tktListSchema.dump(ticket), 200

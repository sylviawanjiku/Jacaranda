from models import MessageModel
from flask_restful import Resource, reqparse, fields, marshal_with, inputs
from database import db
from schema import MessageSchema


msgSchema = MessageSchema()
msgListSchema = MessageSchema(many=True)

message_post_args = reqparse.RequestParser()
message_post_args.add_argument(
    "id", type=int, help="Message ID is required", required=True)
message_post_args.add_argument(
    "message", type=str, help="Message is required", required=True)
message_post_args.add_argument(
    "created", type=str, help="Created-At is required", required=True)
message_post_args.add_argument(
    "updated", type=str, help="Updated-At is required", required=False)
message_post_args.add_argument(
    "user_id", type=int, help="User ID is required", required=True)
message_post_args.add_argument(
    "ticket_id", type=int, help="Ticket ID is required", required=True)
message_post_args.add_argument(
    "incoming", type=inputs.boolean, help="Incoming status is required", required=True)

message_patch_args = reqparse.RequestParser()
message_patch_args.add_argument(
    "id", type=int, help="User ID is required", required=False)
message_patch_args.add_argument(
    "message", type=str, help="Message is required", required=False)
message_patch_args.add_argument(
    "created", type=str, help="Created-At is required", required=False)
message_patch_args.add_argument(
    "updated", type=str, help="Updated-At is required", required=False)
message_patch_args.add_argument(
    "user_id", type=int, help="User id  of the message is required", required=False)
message_patch_args.add_argument(
    "ticket_id", type=int, help="Ticket ID is required", required=False)
message_patch_args.add_argument(
    "incoming", type=inputs.boolean, help="Incoming status is required", required=False)

resource_fields = {
    'id': fields.Integer,
    'message': fields.String,
    'created': fields.String,
    'updated': fields.String,
    'user_id': fields.Integer,
    'ticket_id': fields.Integer,
    'incoming': fields.Boolean,
}

MSG_NOT_FOUND = "Message not found for id: {}"
MSG_DELETE_SUCCESS = "Message deleted successfully for id: {}"


class MessageDetail(Resource):
    def get(self, message_id):
        result = MessageModel.query.filter_by(id=message_id).first()
        if result:
            return msgSchema.dump(result)
        return {'message': MSG_NOT_FOUND.format(message_id)}, 404

    @marshal_with(resource_fields)
    def patch(self, message_id):
        msg_req_json = message_patch_args.parse_args()
        msg_data = MessageModel.query.filter_by(id=message_id).first()
        if msg_data:
            if msg_req_json.get('id', None):
                msg_data.id = msg_req_json['id']
            if msg_req_json.get('message', None):
                msg_data.message = msg_req_json['message']
            if msg_req_json.get('created', None):
                msg_data.created = msg_req_json['created']
            if msg_req_json.get('updated', None):
                msg_data.updated = msg_req_json['updated']
            if msg_req_json.get('user_id', None):
                msg_data.user_id = msg_req_json['user_id']
            if msg_req_json.get('ticket_id', None):
                msg_data.ticket_id = msg_req_json['ticket_id']
            if msg_req_json['incoming'] is not None:
                msg_data.incoming = msg_req_json['incoming']
            db.session.commit()
            return msgSchema.dump(msg_data)
        return {'message': MSG_NOT_FOUND.format(message_id)}, 404

    def delete(self, message_id):
        msg = MessageModel.query.filter_by(id=message_id).delete()
        if msg:
            db.session.commit()
            return {'message': MSG_DELETE_SUCCESS.format(message_id)}, 200
        return {'message': MSG_NOT_FOUND.format(message_id)}, 404


class Message(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = message_post_args.parse_args()
        message = MessageModel(
            id=args["id"],
            message=args["message"],
            created=args["created"],
            updated=args["updated"],
            user_id=args["user_id"],
            ticket_id=args["ticket_id"],
            incoming=args["incoming"]
        )
        db.session.add(message)
        db.session.commit()
        return message, 201

    @marshal_with(resource_fields)
    def get(self):
        msgs = MessageModel.query.all()
        return msgListSchema.dump(msgs), 200

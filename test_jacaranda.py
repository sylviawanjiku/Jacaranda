import pdb
import pytest
import json

from main import create_app, db


ticket = {
    "ticket_id": 2,
    "subject": " And had in was fabled seraphs nor it beyond",
    "phone": 2547900000,
    "intents": "['test', 'test2']"
}
patch_ticket = {
    "ticket_id": 2,
    "subject": " And had in was fabled seraphs nor it beyond",
    "phone": 500000,
    "intents": "['test', 'test2']"
}
message = {
    "id": 2,
    "message": " And had in was fabled seraphs nor it beyond",
    "created": "1639076361000",
    "updated": "1539076361000",
    "user_id": 43012946687,
    "ticket_id": 2,
    "incoming": True
}
fetched_ticket = {
    "ticket_id": 2,
    "subject": " And had in was fabled seraphs nor it beyond",
    "phone": "2547900000",
    "intents": [
        "test",
        "test2"
    ],
    "incoming_messages": [
        {
            "id": 2,
            "message": " And had in was fabled seraphs nor it beyond",
            "created": "1639076361000",
            "updated": "1539076361000",
            "user_id": 43012946687,
            "incoming": True
        }
    ],
    "outgoing_messages": []
}


@pytest.fixture(scope='module')
def test_client():
    app = create_app(config_name='testing')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    # Create a test client using the Flask application configured for testing
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            db.create_all()
            yield testing_client
            db.session.remove()
            db.drop_all()


def test_add_incoming_message(test_client):
    response = test_client.post(
        '/message/',
        data=json.dumps(dict(
            id=2,
            message=" And had in was fabled seraphs nor it beyond",
            created="1639076361000",
            updated="1539076361000",
            user_id=43012946687,
            ticket_id="2",
            incoming=True

        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert data == message


def test_get_messages(test_client):
    response = test_client.get('/message/')
    assert response.status_code == 200


def test_add_ticket(test_client):
    response = test_client.post(
        '/ticket/',
        data=json.dumps(dict(
            ticket_id=2,
            subject=" And had in was fabled seraphs nor it beyond",
            phone="2547900000",
            intents=['test', 'test2']
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert data == ticket


def test_get_ticket(test_client):
    response = test_client.get('/ticket/2', content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data) == fetched_ticket


def test_patch_ticket(test_client):
    response = test_client.patch(
        '/ticket/2',
        data=json.dumps(dict(
            phone="500000",
        )),
        content_type='application/json',
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 200
    assert data == patch_ticket

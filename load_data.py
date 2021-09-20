import json
import re
import pandas as pd

from database import db
from models import TicketModel, MessageModel


# iterate over grouped dataframe and create a dictionary based on ticket_id
def formatRecords(g):
    keys = ['body_text', 'id', 'incoming', 'ticket_id',
            'user_id', 'created_at', 'subject']
    result = []
    for item in g.values.tolist():
        item = dict(zip(keys, item))
        result.append(item)
    return result


def get_intent(ticket_item, intent_list):
    intents = re.split("[:()]", ticket_item["body_text"])[1:2]
    intent_list.append(intents)
    intents = sum(intent_list, [])
    return intents


def load_convert_json_data():
    # load dataset
    df = pd.ExcelFile('Software Developer Interview Assignment (1).xlsx')
    df1 = pd.read_excel(df, 'Messages')
    df2 = pd.read_excel(df, 'Subjects')

    # merge datasets
    maindf = pd.merge(df1, df2, on='ticket_id')
    maindf.head(5)

    # convert to json
    with open('jacaranda_data.json', 'w') as f:
        f.write(maindf.groupby('ticket_id').apply(
            lambda grp: formatRecords(grp)).to_json())

    # Opening JSON file
    f = open('jacaranda_data.json',)

    # returns JSON object as dictionary
    data = json.load(f)
    return data


def load_jacaranda_data():
    data = load_convert_json_data()
    for key, value in data.items():
        intents_list = []
        for ticket_item in value:
            phone = str(re.findall(
                r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]', ticket_item["subject"]))[2:-2]
            subject = re.sub("[\(\[].*?[\)\]]", "", ticket_item["subject"])
            intents = get_intent(ticket_item, intents_list)
            description = re.split("[:()]", ticket_item["body_text"])[-1]
            new_ticket = {
                "ticket_id": ticket_item["ticket_id"],
                "phone": phone if len(phone) > 0 else '',
                "subject": subject,
                "intents": intents
            }
            new_message = {
                "id": ticket_item["id"],
                "user_id": ticket_item["user_id"],
                "ticket_id": ticket_item["ticket_id"],
                "created": ticket_item["created_at"],
                "message": description,
                "incoming": ticket_item["incoming"]

            }
            message = MessageModel(**new_message)
            db.session.add(message)
            db.session.commit()
            ticket = TicketModel(**new_ticket)
            db.session.add(ticket)
            db.session.commit()
    return

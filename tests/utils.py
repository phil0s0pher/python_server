from contextlib import contextmanager
from sqlalchemy import Table, Column, String, MetaData, DateTime, Boolean
from datetime import datetime

metadata = MetaData()
askanything_table = Table('askanythings', metadata,
                          Column('id', String(50), nullable=False),
                          Column('updated_at', DateTime),
                          Column('question', String(500), nullable=False),
                          Column('reviewed', Boolean),
                          Column('authorized', Boolean))

askanything_vote_table = Table('askanythingvotes', metadata,
                               Column('id', String(50), nullable=False),
                               Column(
                                   'question_id', String(50), nullable=False),
                               Column('voter', String(75)))

askanythings_data = [{
    "id": 1,
    "updated_at": datetime.now(),
    "question": "Something",
    "reviewed": True,
    "authorized": True
}, {
    "id": 2,
    "updated_at": datetime.now(),
    "question": "Something Else",
    "reviewed": True,
    "authorized": True
}, {
    "id": 3,
    "updated_at": datetime.now(),
    "question": "Something More",
    "reviewed": True,
    "authorized": True
}]

askanythingvotes_data = [{
    "id": 1,
    "updated_at": datetime.now(),
    "question_id": 1,
    "voter": "ryan.rabello"
}, {
    "id": 2,
    "updated_at": datetime.now(),
    "question_id": 2,
    "voter": "ryan.rabello"
}, {
    "id": 3,
    "updated_at": datetime.now(),
    "question_id": 3,
    "voter": "ryan.rabello"
}]


@contextmanager
def askanything(conn, askanythings=askanythings_data):
    conn.execute(askanything_table.insert(), askanythings)
    yield askanythings
    conn.execute(askanything_table.delete())


@contextmanager
def askanthingvote(conn, askanythingvotes=askanythingvotes_data):
    conn.execute(askanything_vote_table.insert(), askanythingvotes)
    yield askanythingvotes
    conn.execute(askanything_vote_table.delete())

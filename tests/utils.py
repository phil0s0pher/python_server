from contextlib import contextmanager
from sqlalchemy import Table, Column, String, MetaData, DateTime, Boolean
from datetime import datetime
from names import get_first_name, get_last_name


METADATA = MetaData()
ASKANYTHING_TABLE = Table('askanythings', METADATA,
                          Column('id', String(50), nullable=False),
                          Column('updated_at', DateTime),
                          Column('question', String(500), nullable=False),
                          Column('reviewed', Boolean),
                          Column('authorized', Boolean))

ASKANYTHING_VOTE_TABLE = Table('askanythingvotes', METADATA,
                               Column('id', String(50), nullable=False),
                               Column(
                                   'question_id', String(50), nullable=False),
                               Column('voter', String(75)))


def gen_askanythings(number=5):
    for i in xrange(number):
        yield {
            "id": i,
            "updated_at": datetime.now(),
            "question": "Something_{}".format(i),
            "reviewed": True,
            "authorized": True
        }


def gen_askanythingvotes(number=5):
    for i in xrange(number):
        yield {
            "id": i,
            "updated_at": datetime.now(),
            "question_id": 1,
            "voter": get_first_name() + '.' + get_last_name()
        }


def edit(generator, changes):
    for i, record in enumerate(generator):
        if i in changes.iterkeys():
            record.update(changes[i])

        yield record


@contextmanager
def askanything(conn, askanythings=list(gen_askanythings())):

    conn.execute(ASKANYTHING_TABLE.insert(), askanythings)
    yield askanythings
    conn.execute(ASKANYTHING_TABLE.delete())


@contextmanager
def askanthingvote(conn, askanythingvotes=list(gen_askanythingvotes())):
    conn.execute(ASKANYTHING_VOTE_TABLE.insert(), askanythingvotes)
    yield askanythingvotes
    conn.execute(ASKANYTHING_VOTE_TABLE.delete())


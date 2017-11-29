from contextlib import contextmanager
from sqlalchemy import Table, Column, String, MetaData, DateTime, Boolean


metadata = MetaData()
askanything_table = Table('askanythings', metadata,
                          Column('id', String(50), nullable=False),
                          Column('updated_id', DateTime),
                          Column('question', String(500), nullable=False),
                          Column('reviewed', Boolean),
                          Column('authorized', Boolean)
                          )


@contextmanager
def askanything(conn, askanythings):

    conn.execute(askanything_table.insert(), askanythings)
    yield askanythings
    conn.execute(askanything_table.delete())

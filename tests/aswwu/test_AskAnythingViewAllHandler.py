import pytest
import requests
import json

import threading

import tornado.ioloop
from tornado.options import define
import sqlite3

import application


def start_testing_server():
    # pass in the conf default name
    conf_name = "default"

    # initiate the IO loop for Tornado
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.options.parse_config_file("src/aswwu/" + conf_name + ".conf")

    # create thread for running the server
    thread = threading.Thread(
        target=application.start_server, args=(tornado, io_loop))
    thread.daemon = True
    thread.start()

    # allow server to start before running tests
    import time
    time.sleep(1)
    print('starting services...')
    return (io_loop, thread)


def stop_testing_server(io_loop, thread):
    application.stop_server(io_loop)
    thread.join()


@pytest.fixture()
def testing_server():
    (io_loop, thread) = start_testing_server()
    yield
    stop_testing_server(io_loop, thread)


@pytest.fixture()
def test_db():
    data = [(1, "2016-01-01 10:20:05.123", "Somthing", True, True),
            (2, "2016-01-01 10:20:05.124", "Somthing Else", True, True),
            (3, "2016-01-01 10:20:05.125", "Somthing More", True, True)]

    conn = sqlite3.connect(
        '/home/charlie/School/Fall_2017/Software_Testing/labs/python_server/databases/people.db'
    )
    with conn:
        conn.executemany('INSERT INTO askanythings VALUES (?,?,?,?,?)', data)
    yield
    with conn:
        conn.execute('DElETE FROM askanythings')
    conn.close()


def test_No_Data(testing_server):

    expected_data = []

    url = "http://127.0.0.1:8888/askanything/view"
    resp = requests.get(url)
    assert (resp.status_code == 200)
    assert (json.loads(resp.text) == expected_data)


def test_Data(testing_server, test_db):
    expected_data = [{
        u"votes": 0,
        u"reviewed": True,
        u"question": u"Somthing",
        u"authorized": True,
        u"has_voted": False,
        u"question_id": u"1",
    }, {
        u"votes": 0,
        u"reviewed": True,
        u"question": u"Somthing Else",
        u"authorized": True,
        u"has_voted": False,
        u"question_id": u"2",
    }, {
        u"votes": 0,
        u"reviewed": True,
        u"question": u"Somthing More",
        u"authorized": True,
        u"has_voted": False,
        u"question_id": u"3",
    }]

    url = "http://127.0.0.1:8888/askanything/view"
    resp = requests.get(url)
    assert (resp.status_code == 200)
    assert (json.loads(resp.text) == expected_data)

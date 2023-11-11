#!/usr/bin/env python3

from flask import Flask, request, g, jsonify
import time
import sqlite3
import json

RF_QUEUE_FOLDER = '/data/queue'
DATABASE = '/data/biactrl.db'

app = Flask(__name__)

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
        db.row_factory = row_to_dict
    return db

@app.route('/devices', methods = ['GET'])
def get_devices():
    result = get_db().execute('SELECT * FROM devices')
    devices = { 'devices' : result.fetchall() }
    return jsonify(devices)

@app.route('/biactrl', methods = ['POST'])
def hass_device_control():
    xtype = request.form.get('type')
    device = request.form.get('device')
    cmd = request.form.get('cmd')
    tstamp = int(time.time())
    data = { 'type': xtype, 'device': device, 'cmd': cmd, 'time': tstamp }

    json_object = json.dumps(data)
    filename = "{}/{}_{}_{}.json".format(RF_QUEUE_FOLDER, tstamp, xtype, device)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

    return '', 200

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4999, debug=True)
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, send, emit
from serial_reader import serial_getter


app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
# app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins="*")

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@socketio.on('ping')
def handle_message(data):
    """event listener when client types a message"""
    print("got ping")
    emit("pong")

getter = serial_getter()

@socketio.on('start_reading')
def handle_message(data):
    """event listener when client types a message"""
    emit("pong", {'data':'bruh'})
    # print('start reading')
    # value = next(getter)
    # print(value)
    # emit("sensor_reading",{'data':str(value)})
    readings = [0] * 50
    for reading in serial_getter():
        emit("sensor_reading",{'data':str(reading)},broadcast=True)
        readings.append(reading)
        readings.pop()


@socketio.on('connect')
def test_connect():
    print('connected')
    print(request.sid)
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)
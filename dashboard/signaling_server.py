import socketio
import eventlet
import eventlet.wsgi
from flask import flask

sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

@sio.on('join')
def handle_join(sid, data):
    room = data['room']
    sio.enter_room(sid, room)
    sio.emit('user-joined', sid, room=room, skip_sid=sid)

@sio.on('signal')
def handle_signal(sid, data):
    target = data['target']
    signal_data = data['signal']
    sio.emit('signal', {'sid': sid, 'signal': signal_data}, room=target)

@sio.on('disconnect')
def handle_disconnect(sid):
    sio.emit('user-left', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
import random
import string

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"

socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/session')
def session():
    return render_template("session.html")

@socketio.on('join')
def handle_join(sessionId, clientId):
    join_room(sessionId)
    socketio.emit('join', clientId, room=sessionId, include_self=False)

@socketio.on('leave')
def handle_leave(sessionId, clientId):
    leave_room(sessionId)
    socketio.emit('leave', clientId, room=sessionId, include_self=False)

@socketio.on('change_video')
def handle_change_video(sessionId, isPlaying, currentTime):
    socketio.emit(
        'change_video_state',
        data=(isPlaying, currentTime),
        room=sessionId
    )

@socketio.on('set_video')
def handle_set_video(sessionId, id):
    socketio.emit('upload_video', id, room=sessionId)

@socketio.on('send_heartbeat')
def handle_heartbeat(sessionId, id, currentTime, isPlaying, joinedNames):
    socketio.emit(
        'get_heartbeat',
        data=(id, currentTime, isPlaying, joinedNames),
        room=sessionId,
        include_self=False
    )

if __name__ == '__main__':
    socketio.run(app, debug=True)

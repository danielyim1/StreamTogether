from flask import Flask, render_template, request
from datetime import datetime
from flask_socketio import SocketIO, join_room, leave_room
import json
import random
import string

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/session') # ?id=foo
def session():
    # sessionId = request.args.get('id', default = "", type = str)
    # clientId = ''.join(random.choices(string.ascii_uppercase +
                            #  string.digits, k = 10))
    # socketio.enter_room(clientId, sessionId)
    return render_template("session.html")

@socketio.on('join')
def handle_join(sessionId, clientId):
    join_room(sessionId)
    socketio.emit('message', "JoinEvent: " + clientId + " has joined room", room=sessionId, include_self=False)
    print(clientId, sessionId)

@socketio.on('leave')
def handle_leave(sessionId, clientId):
    leave_room(sessionId)
    socketio.emit('message', "LeaveEvent: " + clientId + " has left room", room=sessionId, include_self=False)

@socketio.on('change_video')
def handle_change_video(sessionId, isPlaying,currentTime):
    socketio.emit('change_video_state',data=(isPlaying, currentTime), room=sessionId)

@socketio.on('set_video')
def handle_set_video(sessionId, id):
    socketio.emit('upload_video',id, room=sessionId)

@socketio.on('send_heartbeat')
def handle_heartbeat(sessionId, id, currentTime, isPlaying):
    socketio.emit('get_heartbeat', data=(id, currentTime, isPlaying), room=sessionId, include_self=False)

if __name__ == '__main__':
    socketio.run(app, debug=True)
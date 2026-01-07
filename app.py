from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "change-me-in-production"

socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/session')
def session():
    return render_template("session.html")

# ---------------- Socket.IO Handlers ---------------- #

@socketio.on('join')
def handle_join(data):
    sessionId = data['sessionId']
    clientId = data['clientId']
    join_room(sessionId)
    socketio.emit('join', clientId, room=sessionId, include_self=False)

@socketio.on('leave')
def handle_leave(data):
    sessionId = data['sessionId']
    clientId = data['clientId']
    leave_room(sessionId)
    socketio.emit('leave', clientId, room=sessionId, include_self=False)

@socketio.on('change_video')
def handle_change_video(data):
    sessionId = data['sessionId']
    isPlaying = data['isPlaying']
    currentTime = data['currentTime']
    socketio.emit(
        'change_video_state',
        {'isPlaying': isPlaying, 'currentTime': currentTime},
        room=sessionId
    )

@socketio.on('set_video')
def handle_set_video(data):
    sessionId = data['sessionId']
    video_id = data['id']
    socketio.emit('upload_video', video_id, room=sessionId)

@socketio.on('send_heartbeat')
def handle_heartbeat(data):
    sessionId = data['sessionId']
    video_id = data['id']
    currentTime = data['currentTime']
    isPlaying = data['isPlaying']
    joinedNames = data['joinedNames']
    socketio.emit(
        'get_heartbeat',
        {'id': video_id, 'currentTime': currentTime, 'isPlaying': isPlaying, 'joinedNames': joinedNames},
        room=sessionId,
        include_self=False
    )

@socketio.on('send_message')
def handle_message(data):
    sessionId = data['sessionId']
    clientId = data['clientId']
    message = data['message']
    socketio.emit(
        'receive_message',
        {'clientId': clientId, 'message': message},
        room=sessionId
    )

# ---------------- Run App ---------------- #

if __name__ == '__main__':
    socketio.run(app, debug=True)
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
    # print(render_template("home.html"))
    return render_template("home.html")

@app.route('/session') # ?id=foo
def session():
    # sessionId = request.args.get('id', default = "", type = str)
    # clientId = ''.join(random.choices(string.ascii_uppercase +
                            #  string.digits, k = 10))
    # socketio.enter_room(clientId, sessionId)
    return render_template("session.html")

# @app.route('/synconline')
# def sync():
#     data = {"Time": datetime.now().strftime("%H:%M:%S")}
#     return json.dumps(data)

@socketio.on('join')
def handle_join(sessionId, clientId):
    join_room(sessionId)
    socketio.emit('message', clientId + " has joined room", room=sessionId)
    print(clientId, sessionId)

@socketio.on('leave')
def handle_leave(sessionId, clientId):
    leave_room(sessionId)
    socketio.emit('message', clientId + " has left room", room=sessionId)

@socketio.on('change_video')
def handle_change_video(sessionId, isPlaying,currentTime):
    socketio.emit('change_video_state',data= (isPlaying,currentTime), room=sessionId)


@socketio.on('set_video')
def handle_set_video(sessionId, link):
    # https://www.youtube.com/watch?v=OPaGNHYR8fg&feature=emb_logo
    # https://www.youtube.com/embed/OPaGNHYR8fg
    starting = link.find('?v=') + 3
    if starting != 2:
        id = link[starting:]
        if id.find('&') != -1:
            id = id[:id.find('&')] 
        # newLink = "https://www.youtube.com/embed/" + id
        # print(newLink)
        # print()
    else:
        # newLink="Invalid"
        id = "Invalid"
        print("Invalid video id")
        print()
    socketio.emit('upload_video',id, room=sessionId)
if __name__ == '__main__':
    socketio.run(app, debug=True)
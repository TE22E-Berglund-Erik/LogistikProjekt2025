from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('message')
def handle_msg(msg):
    full_msg = f"Server received: {msg}"
    print(full_msg)
    send(full_msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
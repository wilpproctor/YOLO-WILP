import eventlet
import socketio
import os

from blur import blur_check
from detect import analyze

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

MOCK_AI = os.getenv("MOCK_AI") == "true"

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def webcam(sid, data):
    if MOCK_AI:
        return {
            "blurry": False,
            "detected": [{
                "type": "person",
                "coords": [0,0,0,0],
                "conf": 1
            }]
        }
    output = {
        "blurry": blur_check(data),
        "detected": analyze(data)
    }
    return output

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), app)

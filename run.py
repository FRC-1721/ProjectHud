import logging

import eventlet

eventlet.monkey_patch()

from app import create_app, db, socketio

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = create_app()

if __name__ == "__main__":
    socketio.run(app, debug=True)

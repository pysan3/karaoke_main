# import sys
# import json
# from websocket_server import WebsocketServer

# import app as backapp
# ws_audio = backapp.WebSocketApp()

# def new_client(client, server):
#     ws_audio.new_client()
#     print('created connection')

# def client_left(client, server):
#     ws_audio.close('hoge')
#     print('disconnected')

# def ws_upload(client, server, message):
#     print(message)
#     song = json.loads(message)
#     music = song['music']
#     ws_audio.upload(music)
#     result = json.dumps({'success':ws_audio.return_counter()})
#     server.send_message(client, result)

# server = WebsocketServer(8000, host='localhost')
# server.set_fn_new_client(new_client)
# server.set_fn_client_left(client_left)
# server.set_fn_message_received(ws_upload)
# server.run_forever()

from flask import Flask, request, make_response, jsonify
import os
import werkzeug
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = os.getenv("UPLOAD_DIR_PATH")

@app.route('/api/upload', methods=['POST'])
def upload_multipart():
    print(request.files['music'])
    # if 'uploadFile' not in request.files:
    #     make_response(jsonify({'result':'uploadFile is required.'}))
    # file = request.files['uploadFile']
    # fileName = file.filename
    # if '' == fileName:
    #     make_response(jsonify({'result':'filename must not empty.'}))
    # saveFileName = datetime.now().strftime("%Y%m%d_%H%M%S_") \
    #     + werkzeug.utils.secure_filename(fileName)
    # file.save(os.path.join(UPLOAD_DIR, saveFileName))
    # return make_response(jsonify({'result':'upload OK.'}))

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    return 'result : file size is overed.'

# main
if __name__ == "__main__":
    print(app.url_map)
    app.run(host='localhost', port=5042)
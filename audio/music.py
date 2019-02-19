import numpy as np
import wave
from glob import glob

from audio import analyze, network

def load_music(song_id):
    if song_id in [s[10:-4] for s in glob('audio/wav/*.wav')]:
        with open('audio/wav/{0}.wav'.format(song_id), 'rb') as f:
            return f.read()
    else:
        return False

def upload(song_id, data):
    # TODO: format data
    with open('audio/wav/{0}.wav'.format(song_id), 'wb') as f:
        f.write(data)
    analyze.create_hash(data[44:])

class WebSocketApp:
    def __init__(self):
        self.data = []
        self.stream_data = []
        self.counter = 0

    def upload(self, stream):
        self.counter += 1
        self.data.append((np.frombuffer(stream, dtype='float32') * 32767).astype(np.int16))
        self.stream_data.append((np.frombuffer(stream, dtype='float32')).tolist())

    def return_counter(self):
        return self.counter

    def close(self, info):
        v = np.array(self.data).flatten()
        with wave.Wave_write('hoge.wav') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(info['framerate'])
            wf.writeframes(v.tobytes('C'))

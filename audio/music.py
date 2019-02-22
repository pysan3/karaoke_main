#pylint: skip-file
import numpy as np
import scipy as sp
import wave
import os
from glob import glob
import sox

from audio import analyze, network

def load_music(song_id):
    if song_id in [s[12:-4] for s in glob('./audio/wav/*.wav')]:
        with open('./audio/wav/{0}.wav'.format(song_id), 'rb') as f:
            return f.read()
    else:
        return False

def upload(song_id, data, ftype):
    # TODO: check whether wav
    with open('./audio/wav/tmp_{0}.{1}'.format(song_id, ftype), 'wb') as f:
        f.write(data)
    tfm = sox.Transformer()
    tfm.set_output_format(file_type='wav', rate=48000, bits=16, channels=1)
    tfm.build('./audio/wav/tmp_{0}.{1}'.format(song_id, ftype), './audio/wav/{0}.wav'.format(song_id))
    os.remove('./audio/wav/tmp_{0}.{1}'.format(song_id, ftype))
    with open('{0}.wav'.format(song_id), 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16')
    # => [(hsh, start_time), ...]
    return create_hash(data)

def create_hash(data):
    f, t = analyze.find_peaks(data.astype(float) / 32767)
    return analyze.peaks_to_landmarks(f, t)
    # => list_hsh, list_ptime (both in str)

class WebSocketApp:
    def __init__(self):
        self.data = []
        self.stream_data = []
        self.counter = 0

    def upload(self, stream):
        self.counter += 1
        self.data.append(np.frombuffer(stream, dtype='float32'))

    def return_counter(self):
        return self.counter

    def close(self, info):
        v = (np.array(self.data).flatten() * 32767).astype(np.int16)
        with wave.Wave_write('hoge.wav') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(info['framerate'])
            wf.writeframes(v.tobytes('C'))
        with open('hoge.txt', mode='wb') as f:
            f.write(v.tobytes('C'))

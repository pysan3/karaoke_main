#pylint: skip-file
import numpy as np
import scipy as sp
import wave
from fractions import Fraction
from struct import unpack
import os
from glob import glob
import sox
import soundfile

from audio import analyze, network

def load_music(song_id):
    if song_id in [s[10:-4] for s in glob('audio/wav/*.wav')]:
        with open('audio/wav/{0}.wav'.format(song_id), 'rb') as f:
            return f.read()
    else:
        return False

def upload(song_id, data):
    # TODO: check whether wav
    with open('audio/wav/tmp_{0}.wav'.format(song_id), 'wb') as f:
        f.write(data)
    tfm = sox.Transformer()
    # tfm.convert(samplerate=48000, n_channels=1, bitdepth=16)
    tfm.set_output_format(file_type='wav', rate=48000, bits=16, channels=1)
    tfm.build('audio/wav/tmp_{0}.wav'.format(song_id), '{0}.wav'.format(song_id))
    with open('{0}.wav'.format(song_id), 'rb') as f:
        data = f.read()
    sampwidth = int.from_bytes(data[34:36], byteorder='little') // 8
    nchannels = int.from_bytes(data[22:24], byteorder='little')
    framerate = int.from_bytes(data[24:28], byteorder='little')
    print(sampwidth, nchannels, framerate)
    os.remove('audio/wav/tmp_{0}.wav'.format(song_id))
    # => [(hsh, start_time), ...]
    # return create_hash(data)

def check_tfm(songname, filetype):
    tfm = sox.Transformer()
    tfm.set_output_format(file_type='wav', rate=48000, bits=16, channels=1)
    tfm.build('audio/wav/{0}.{1}'.format(songname, filetype), '{0}.wav'.format(songname))

def create_hash(data):
    f, t = analyze.find_peaks(np.array(data) / 32767)
    landmarks = analyze.peaks_to_landmarks(f, t)
    return landmarks

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

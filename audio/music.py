import numpy as np
import scipy as sp
import wave
import os
from time import sleep
from glob import glob
import sox

from audio import analyze

def load_music(song_id):
    if song_id in [s[13:-4] for s in glob('./audio/inst/*.wav')]:
        with open('./audio/inst/{0}.wav'.format(song_id), 'rb') as f:
            return f.read()
    else:
        return False

def upload(song_id, data, ftype):
    with open('./audio/wav/tmp_{0}.{1}'.format(song_id, ftype), 'wb') as f:
        f.write(data)
    tfm = sox.Transformer()
    tfm.set_output_format(file_type='wav', rate=16000, bits=16, channels=1)
    if tfm.build('./audio/wav/tmp_{0}.{1}'.format(song_id, ftype), './audio/wav/{0}.wav'.format(song_id)):
        os.remove('./audio/wav/tmp_{0}.{1}'.format(song_id, ftype))
        separate_audio(song_id)
        return True
    else:
        return False

def upload_hash(song_id):
    with open('./audio/wav/{0}.wav'.format(song_id), 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16')[:1024*50*5]
    return create_hash(data.astype(np.float32) / 32676)

def separate_audio(song_id):
    unet = analyze.UNet()
    mag, phase, length = analyze.load_audio('./audio/wav/{0}.wav'.format(song_id))
    vocal = []
    inst = []
    for i in range(0, mag.shape[1], 1024):
        mask = analyze.compute_mask(unet, mag[:, i:i+1024])
        vocal.append(analyze.save_audio(mag[:, i:i+1024]*mask, phase[:, i:i+1024]))
        inst.append(analyze.save_audio(mag[:, i:i+1024]*(1-mask), phase[:, i:i+1024]))
    analyze.write_wav('./audio/vocal/{0}.wav'.format(song_id), np.array(vocal).flatten()[:length], 16000, norm=True)
    analyze.write_wav('./audio/inst/{0}.wav'.format(song_id), np.array(inst).flatten()[:length], 16000, norm=True)

def create_hash(data):
    f, t = analyze.find_peaks(data)
    return analyze.peaks_to_landmarks(f, t)
    # => list_hsh, list_ptime (both in str)

class WebSocketApp:
    def __init__(self, tpl):
        self.data = []
        self.counter = 0
        self.hsh_data = [int(i) for i in tpl[0].split()]
        self.ptime = [int(i) for i in tpl[1].split()]

    def upload(self, stream):
        self.data.append(np.frombuffer(stream, dtype='float32'))
        self.counter += 1

    def lag_estimate(self):
        hsh, ptime = tuple(list(map(int, l.split())) for l in create_hash(np.array(self.data).flatten()[:1024*50*5]))
        lag_dict = {0:0}
        for i in range(len(hsh)):
            if hsh[i] in self.hsh_data:
                lag = ptime[i] - self.ptime[self.hsh_data.index(hsh[i])]
                if lag in lag_dict.keys():
                    lag_dict[lag] += 1
                else:
                    lag_dict[lag] = 1
        poss_lag = max(lag_dict.values())
        if poss_lag > 0:
            self.lag = [k for k, v in lag_dict.items() if v == poss_lag][0]
            return True
        else:
            return False
        # TODO: erase below before publication
        with open('lag.txt', mode='w') as f:
            f.write('rank : lag (possibility)\n')
            poss_lag = 2
            i = 1
            while poss_lag != 1 and i < 10:
                poss_lag = max(lag_dict.values())
                usual_lag = [k for k, v in lag_dict.items() if v == poss_lag][0]
                f.write('   {0} : {1} ({2}) ... {3}\n'.format(i, usual_lag, poss_lag, self.counter))
                lag_dict.pop(usual_lag)
                i += 1

    def check_lag(self):
        return self.counter == 50 * 5

    def return_counter(self):
        return self.counter, self.lag

    def close(self, info):
        v = (np.array(self.data).flatten() * 32767).astype(np.int16)
        with wave.Wave_write('hoge.wav') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(info['framerate'])
            wf.writeframes(v.tobytes('C'))
        print(self.lag)

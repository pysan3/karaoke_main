import numpy as np
import scipy as sp
import wave
import matplotlib.pyplot as plt
from time import time

import audio.music as backmusic
from audio import analyze

import cProfile

def main():
    with open('lag.txt', 'r') as f:
        lags = [(int(l.strip().split()[2]), int(l.strip().split()[3][1:-1])) for l in f.readlines()[1:]]
    lag = lags[0][0] * lags[0][1]
    count = lags[0][1]
    i = 1
    while abs(lags[i-1][0] - lags[i][0]) < 5:
        lag += lags[i][0] * lags[i][1]
        count += lags[i][1]
        i += 1
    lag /= count
    print(lag, i)
    x = np.arange(0, 256000 / 48000, 1.0 / 48000)
    with open('hoge.wav', 'rb') as f:
        data = f.read()
        hoge = np.frombuffer(data[44:], dtype='int16').astype(np.float32) / 32676
        hoge = hoge[:256000]
        plt.subplot(3, 1, 1)
        plt.plot(x, hoge)
    with open('audio/wav/8.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
        data = data[:256000]
        plt.subplot(3, 1, 2)
        plt.plot(x, data)
    test = hoge[round(lag*512/4):]
    zero = []
    # check params
    y = sp.signal.firwin(511, 0.9)
    for i in range(0, len(test), 1024):
        zero.append(data[i:i+1024:3])
    zero = np.array(zero).flatten()
    # zero = np.zeros(256000)
    # delta = max(test) / max(data)
    # for i in range(len(test)):
    #     zero[i] = test[i] - data[i] * delta
    plt.subplot(3, 1, 3)
    plt.plot(zero)
    with wave.Wave_write('lag_correction.wav') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(16000)
        w.writeframes((zero * 32676).astype(np.int16).tobytes('C'))
    plt.show()

def separate_whole_audio_data():
    unet = analyze.UNet()
    unet.load()
    mag, phase = analyze.load_audio('audio/wav/8.wav')
    vocal = []
    inst = []
    start = time()
    for i in range(0, mag.shape[1]-1024, 1024):
        mask = analyze.compute_mask(unet, mag[:, i:i+1024])
        vocal.append(analyze.save_audio(mag[:, i:i+1024]*mask, phase[:, i:i+1024]))
        inst.append(analyze.save_audio(mag[:, i:i+1024]*(1-mask), phase[:, i:i+1024]))
    from librosa.output import write_wav
    write_wav('vocal.wav', np.array(vocal).flatten(), 16000, norm=True)
    write_wav('inst.wav', np.array(inst).flatten(), 16000, norm=True)
    print(time() - start)


# pr = cProfile.Profile()
# pr.runcall(main)
# pr.print_stats()

# main()

separate_whole_audio_data()

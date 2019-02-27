import numpy as np
import wave
import matplotlib.pyplot as plt

import audio.music as backmusic
from audio import analyze

import cProfile

def main():
    with open('audio/wav/2.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
    usual_hsh_data, usual_ptime = tuple([int(i) for i in l.split()] for l in backmusic.create_hash(data))
    print(len(usual_hsh_data))
    with open('hoge.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
    hsh, ptime = tuple([int(i) for i in l.split()] for l in backmusic.create_hash(data[:1024*2000]))
    print(len(hsh))
    lag_dict = {0:0}
    for i in range(len(hsh)):
        if hsh[i] in usual_hsh_data:
            lag = ptime[i] - usual_ptime[usual_hsh_data.index(hsh[i])]
            if lag in lag_dict.keys():
                lag_dict[lag] = lag_dict[lag] ** 2 + 1
            else:
                lag_dict[lag] = 0
    print(lag_dict)
    poss_lag = max(lag_dict.values())
    print(poss_lag)
    if poss_lag > 0:
        usual_lag = [k for k, v in lag_dict.items() if v == poss_lag][0]
        print(usual_lag)

def correlate():
    with open('audio/wav/2.wav', 'rb') as f:
        pre = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
    plt.subplot(2, 1, 1)
    plt.ylabel('pre')
    plt.plot(pre)
    with open('hoge.wav', 'rb') as f:
        record = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
    plt.subplot(2, 1, 2)
    plt.ylabel('record')
    plt.plot(record)
    plt.show()
    pre = pre[:2000]
    record = record[:2000]
    if pre.mean():
        print('pre not zero')
        pre -= pre.mean()
    if record.mean():
        print('record ave not zero')
        record -= record.mean()
    corr = np.correlate(pre, record, 'full')
    estimate_delay = corr.argmax() - len(record) + 1
    print(estimate_delay)

# pr = cProfile.Profile()
# pr.runcall(correlate)
# pr.print_stats()

correlate()
main()

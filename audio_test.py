import numpy as np
import wave
import matplotlib.pyplot as plt

import audio.music as backmusic
from audio import analyze

import cProfile

def main():
    with open('hoge.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
    hsh, ptime = tuple(list(map(int, l.split())) for l in backmusic.create_hash(data[:1024*50*5]))
    print(len(hsh))
    with open('audio/wav/3.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16').astype(np.float32) / 32676
    usual_hsh_data, usual_ptime = tuple(list(map(int, l.split())) for l in backmusic.create_hash(data[:1024*50*5]))
    print(len(usual_hsh_data))
    lag_dict = {0:0}
    for i in range(len(hsh)):
        if hsh[i] in usual_hsh_data:
            lag = ptime[i] - usual_ptime[usual_hsh_data.index(hsh[i])]
            if lag in lag_dict.keys():
                lag_dict[lag] += 1
            else:
                lag_dict[lag] = 1
    print('rank : lag (possibility)')
    poss_lag = 2
    i = 1
    while poss_lag != 1 and i < 10:
        poss_lag = max(lag_dict.values())
        usual_lag = [k for k, v in lag_dict.items() if v == poss_lag][0]
        print('   {0} : {1} ({2})'.format(i, usual_lag, poss_lag))
        lag_dict.pop(usual_lag)
        i += 1

def correlate():
    with open('audio/wav/3.wav', 'rb') as f:
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

# correlate()
main()

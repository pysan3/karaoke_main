import numpy as np
import wave

import audio.music as backmusic
from audio import analyze

import cProfile

def main():
    with open('audio/wav/11.wav', 'rb') as f:
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
                lag_dict[lag] += 1
            else:
                lag_dict[lag] = 1
    print(lag_dict)
    poss_lag = max(lag_dict.values())
    print(poss_lag)
    if poss_lag > 0:
        usual_lag = [k for k, v in lag_dict.items() if v == poss_lag][0]
        print(usual_lag)


# pr = cProfile.Profile()
# pr.runcall(main)
# pr.print_stats()

main()

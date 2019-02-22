import numpy as np
import wave

import audio.music as backmusic
from audio import analyze

import cProfile

def main():
    with open('./audio/wav/2.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16')
    lm = backmusic.create_hash(data)
    if len(lm) == 0:
        print('no data')
    print(len(lm))

pr = cProfile.Profile()
pr.runcall(main)
pr.print_stats()

# main()
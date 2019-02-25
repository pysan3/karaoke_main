import numpy as np
import wave

import audio.music as backmusic
from audio import analyze

import cProfile

def main():
    with open('./audio/wav/2.wav', 'rb') as f:
        data = np.frombuffer(f.read()[44:], dtype='int16')
    lm = backmusic.create_hash(data.astype(np.float32) / 32676)
    print(len(lm[0].split()))

pr = cProfile.Profile()
pr.runcall(main)
pr.print_stats()

# main()
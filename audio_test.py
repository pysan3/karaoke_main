import numpy as np
import wave

import audio.music as backmusic
from audio import analyze

def main():
    with open('./audio/wav/2.wav', 'rb') as f:
        data = f.read()
    lm = backmusic.create_hash(data)
    print(lm)

main()
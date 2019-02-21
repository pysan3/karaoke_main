import numpy as np
import wave

import audio.music as backmusic
from audio import analyze

def main():
    # with open('./audio/data.txt', 'rb') as f:
    #     data = f.read()
    # landmarks = backmusic.create_hash(np.array(data).flatten())
    # print(landmarks)
    file_list = ['trumpet', 'sei', 'piano', 'test']
    file_type = ['wav', 'wav', 'wav', 'mp3']
    for fname, ftype in zip(file_list, file_type):
        print('working on', fname, ftype)
        backmusic.check_tfm(fname, ftype)
        # with open('./audio/wav/{0}.wav'.format(fname), 'rb') as f:
        #     data = f.read()
        # backmusic.upload(fname, data)

main()
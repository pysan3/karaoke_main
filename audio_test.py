import numpy as np

import audio.music as backmusic
from audio import analyze

def main():
    with open('/audio/data.txt', 'r') as f:
        data = [[float(i) for i in j.split(', ')] for j in f.read()[2:-2].split('], [')]
    peaks_freq, peaks_time = analyze.find_peaks(np.array(data).flatten())
    for i in range(len(peaks_freq)):
        print(data[peaks_freq[i]][peaks_time[i]])

main()
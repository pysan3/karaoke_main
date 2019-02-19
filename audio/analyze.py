import wave
import numpy as np
import scipy.ndimage as ndi
import scipy.ndimage.morphology as mor
from librosa.core import stft

def create_hash(data):
    pass

def find_peaks(y):
    sgram = np.array(np.abs(stft(y, n_fft=512, hop_length=256)))
    sgram = np.where(sgram==0, 0, 10 * np.log(sgram))
    neighborhood = mor.iterate_structure(mor.generate_binary_structure(2, 1), 20)
    sgram_max = ndi.maximum_filter(sgram, footprint=neighborhood, mode='constant')
    maxima = (sgram==sgram_max) & (sgram > 0.2)
    peaks_freq, peaks_time = np.asarray(maxima).nonzero()
    print(peaks_freq, peaks_time)
    return peaks_freq, peaks_time

def peaks_to_landmarks(peaks_freq,peaks_time):
    peak_mat = np.zeros((np.max(peaks_freq)+30,np.max(peaks_time)+60),dtype=np.bool)
    peak_mat[peaks_freq,peaks_time] = True
    list_landmarks = []
    for pfreq,ptime in zip(peaks_freq,peaks_time):
        #(pfreq,ptime) -- current anchor
        target_mask = np.zeros(peak_mat.shape,dtype=np.bool)
        target_mask[pfreq-30 : pfreq+30, ptime+30 : 60] = 1
        #target_mask:target peakを選ぶ範囲を指定する
        targets_freq, targets_time = np.asarray(peak_mat & target_mask).nonzero()
        for pfreq_target,ptime_target in zip(targets_freq, targets_time):
            dtime = ptime_target-ptime
            #ハッシュを構築
            hsh = (((pfreq & 255)<<12) | (((pfreq_target+30-pfreq)&63)<<6)|(dtime&63))
            list_landmarks.append((hsh,ptime))   #ハッシュとピーク1の時間を保存
    return list_landmarks

def main():
    with open('/audio/data.txt', 'r') as f:
        data = [[float(i) for i in j.split(', ')] for j in f.read()[2:-2].split('], [')]
    peaks_freq, peaks_time = find_peaks(np.array(data).flatten())
    for i in range(len(peaks_freq)):
        print(data[peaks_freq[i]][peaks_time[i]])


if __name__ == '__main__':
    main()
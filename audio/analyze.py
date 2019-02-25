import numpy as np
import scipy.ndimage as ndi
from librosa.core import stft

def find_peaks(data):
    sgram = np.abs(stft(data, n_fft=1024, window='hamming'))
    neighborhood = ndi.morphology.iterate_structure(ndi.morphology.generate_binary_structure(2, 1), 20)
    sgram_max = ndi.maximum_filter(sgram, footprint=neighborhood, mode='constant')
    # => (peaks_freq, peaks_time)
    return np.asarray((sgram==sgram_max) & (sgram > 0.2)).nonzero()

def peaks_to_landmarks(peaks_freq, peaks_time):
    peak_mat = np.zeros((np.max(peaks_freq)+30, np.max(peaks_time)+260), dtype=np.bool)
    peak_mat[peaks_freq, peaks_time] = True
    list_hsh = ''
    list_ptime = ''
    for pfreq, ptime in zip(peaks_freq, peaks_time):
        target_mask = np.zeros(peak_mat.shape, dtype=np.bool)
        target_mask[(pfreq-30 if pfreq >= 30 else 0) : pfreq+30, ptime+20 : ptime+260] = True
        targets_freq, targets_time = np.asarray(peak_mat & target_mask).nonzero()
        for pfreq_target, ptime_target in zip(targets_freq, targets_time):
            dtime = ptime_target - ptime
            hsh = (((pfreq & 511)<<12) | ((pfreq_target&63)<<6) | (dtime&63))
            list_hsh += str(hsh) + ' '
            list_ptime += str(ptime) + ' '
    return list_hsh[:-1], list_ptime[:-1]

from glob import glob

import numpy as np
from chainer import config
from librosa.core import stft, load, istft
from librosa.output import write_wav
import os.path

import network
import const as C

def load_music(song_id):
    if song_id in [s[10:-4] for s in glob('audio/wav/*.wav')]:
        with open('audio/wav/{0}.wav'.format(song_id), 'rb') as f:
            return f.read()
    else:
        return False

def upload(song_id, data):
    with open('audio/wav/{0}.wav'.format(song_id), 'wb') as f:
        f.write(data)

def LoadAudio(fname):
    y, _ = load(fname, sr=C.SR)
    spec = stft(y, n_fft=C.FFT_SIZE, hop_length=C.H, win_length=C.FFT_SIZE)
    mag = np.abs(spec)
    mag /= np.max(mag)
    phase = np.exp(1.j*np.angle(spec))
    return mag, phase

def SaveAudio(fname, mag, phase):
    y = istft(mag*phase, hop_length=C.H, win_length=C.FFT_SIZE)
    write_wav(fname, y, C.SR, norm=True)

def ComputeMask(input_mag, unet_model="unet.model", hard=True):
    unet = network.UNet()
    unet.load(unet_model)
    config.train = False
    config.enable_backprop = False
    mask = unet(input_mag[np.newaxis, np.newaxis, 1:, :]).data[0, 0, :, :]
    mask = np.vstack((np.zeros(mask.shape[1], dtype="float32"), mask))
    if hard:
        hard_mask = np.zeros(mask.shape, dtype="float32")
        hard_mask[mask > 0.5] = 1
        return hard_mask
    else:
        return mask

def receive_stream(stream):
    mag, phase = LoadAudio(fname)
    start

folder = './wav/'
fname = "original_mix.wav"
mag, phase = LoadAudio(folder + fname)
start = 1024
end = 1024+1024

mask = ComputeMask(mag[:, start:end], unet_model="unet.model", hard=False)

SaveAudio(
    folder + "vocal-%s" % fname, mag[:, start:end]*mask, phase[:, start:end])
SaveAudio(
    folder + "inst-%s" % fname, mag[:, start:end]*(1-mask), phase[:, start:end])
SaveAudio(
    folder + "orig-%s" % fname, mag[:, start:end], phase[:, start:end])

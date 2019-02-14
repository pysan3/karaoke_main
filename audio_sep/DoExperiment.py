import util

"""
Code example for training U-Net
"""

"""
import network

Xlist,Ylist = util.LoadDataset(target="vocal")
print("Dataset loaded.")
network.TrainUNet(Xlist,Ylist,savefile="unet.model",epoch=30)
"""


"""
Code example for performing vocal separation with U-Net
"""
folder = './wav/'
fname = "original_mix.wav"
mag, phase = util.LoadAudio(folder + fname)
start = 2048
end = 2048+1024

mask = util.ComputeMask(mag[:, start:end], unet_model="unet.model", hard=False)

util.SaveAudio(
    folder + "vocal-%s" % fname, mag[:, start:end]*mask, phase[:, start:end])
util.SaveAudio(
    folder + "inst-%s" % fname, mag[:, start:end]*(1-mask), phase[:, start:end])
util.SaveAudio(
    folder + "orig-%s" % fname, mag[:, start:end], phase[:, start:end])

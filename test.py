import os
from time import sleep
import wave
from glob import glob

for f in glob('*1.wav'):
    os.system(f'del {f}')

# for f in glob('*.wav'):
#     with wave.open(f, 'rb') as wf:
#         print(f)
#         channel = wf.getnchannels()
#         width = wf.getsampwidth()
#         frate = wf.getframerate()
#         data = wf.readframes(wf.getnframes())
#     print(channel, width, frate)
#     w = wave.Wave_write(f[:-4] + '1.wav')
#     w.setnchannels(channel)
#     w.setsampwidth(width)
#     w.setframerate(frate)
#     w.writeframes(data)
#     w.close()

for f in glob('*.wav'):
    with wave.open(f, 'rb') as wf:
        print(f)
        print(wf.getnchannels())
        print(wf.getsampwidth())
        print(wf.getframerate())
        print(wf.readframes(wf.getnframes())[:50])
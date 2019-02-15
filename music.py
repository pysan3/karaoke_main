from glob import glob

def load_music(song_id):
    if song_id in [s[10:-4] for s in glob('audio/wav/*.wav')]:
        with open('audio/wav/{0}.wav'.format(song_id), 'rb') as f:
            return f.read()
    else:
        return False

def upload(song_id, data):
    with open('audio/wav/{0}.wav'.format(song_id), 'wb') as f:
        f.write(data)

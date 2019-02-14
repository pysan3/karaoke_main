def load_music(song_id):
    with open('audio/wav/{0}.wav'.format(song_id), 'rb') as f:
        return f.read()

def upload(song_id, data):
    with open('audio/wav/{0}.wav'.format(song_id), 'wb') as f:
        f.write(data)

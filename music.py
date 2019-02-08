import wave

def upload(song_id, data):
    print('sampwidth:', int.from_bytes(data[34:36] / 8, byteorder='little'))
    print('channel', int.from_bytes(data[22:24], byteorder='little'))
    print('framerate', int.from_bytes(data[24:28], byteorder='little'))
    # fname = 'audio/wav/{0}.wav'.format(song_id)
    # w = wave.Wave_write(fname)
    # w.setnchannels(int.from_bytes(data[22:24], byteorder='little'))
    # w.setsampwidth(int.from_bytes(data[34:36] / 8, byteorder='little'))
    # w.setframerate(int.from_bytes(data[24:28], byteorder='little'))
    # w.writeframes(data)
    # w.close()
    return 1
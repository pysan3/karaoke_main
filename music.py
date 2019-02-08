import wave

def upload(song_id, data):
    fname = 'audio/wav/{0}.wav'.format(song_id)
    w = wave.Wave_write(fname)
    w.setnchannels(int.from_bytes(data[22:24], byteorder='little'))
    w.setsampwidth(int.from_bytes(data[34:36], byteorder='little') // 8)
    w.setframerate(int.from_bytes(data[24:28], byteorder='little'))
    w.writeframes(data)
    w.close()
    return 1
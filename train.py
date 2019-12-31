import os
import scipy.io.wavfile as wavfile
import numpy as np
import matplotlib.pyplot as plt
import webrtcvad
import struct

def get_files(directory, ext=".wav"):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1] == ext:
                file_list.append(os.path.join(root, file))
    return file_list

def preprocessing(file_list, feature="mfcc"):
    pass

def read_wav(filename):
    fs, x = wavfile.read(filename = filename)
    x = np.array(x)/32768
    return fs, x

def write_wav(filename, rate, data):
    data = np.clip(data, -1, 1)
    data = data * 32767
    data = data.astype("int16")
    wavfile.write(filename=filename, rate=rate, data=data)
"""
x: A numpy array containing mono audio samples ([-1, 1]). 
"""
def to_binary_pcm(x):
    x = x * 32767
    x = x.astype("int16")
    out = bytearray()
    for xx in x:
        if xx < 0:
            xx += 65536
        out += int(xx).to_bytes(2, "little")
    return out

def vad(x, fs):
    step = 240
    vad_obj = webrtcvad.Vad(3)
    
    
    flags = []
    frames = [x[i:i + 480] for i in range(0, len(x)-480, step)]
    for frame in frames:
        if vad_obj.is_speech(to_binary_pcm(frame), fs):
            flags.extend([1]*step)
        else:
            flags.extend([0]*step)
    
    flags.extend([0]*(len(x)-len(flags)))
    return flags
    
if  __name__ == "__main__":
    file_list = get_files(directory="train_data", ext=".wav")
    
    fs, x = read_wav(filename=file_list[0])

    print()
    plt.figure()
    plt.plot(x)
    plt.plot(vad(x, fs))
    plt.show()



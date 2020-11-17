import playsound
import sounddevice as sd
import wavio
from pydub import AudioSegment
import subprocess
import acoustid
import soundfile as sf
import librosa
import dtw
from numpy.linalg import norm
import numpy as np

def record_audio(name, duration):
    print("recording")
    fs = 44100
    audio = sd.rec(int(fs * duration), samplerate = fs, channels = 2)
    sd.wait()
    wavio.write(name + ".wav", audio, fs, sampwidth = 2)
    trim_audio(name)

def speak_audio(audio):
    # stretch_audio(audio, 10)
    print("speaking: length of", len(AudioSegment.from_wav(audio + ".wav")))
    playsound.playsound(audio + ".wav")

def trim_audio(name):
    audio = AudioSegment.from_wav(name + ".wav")
    trimmed_audio = remove_silence(audio)
    trimmed_audio.export(name + ".wav", format="wav")
    

def stretch_audio(name, time):
    y, sr = librosa.load(name + ".wav")
    duration = librosa.get_duration(y=y, sr=sr)
    # print(duration, len(y), sr)
    # print(duration, sr)
    new_y = librosa.effects.time_stretch(y, duration/time)
    sf.write(name + ".wav", new_y.T, sr)
    # librosa.output.write_wav(name + ".wav", new_y, sr)

def MFCC(audio):
    if audio == "blank":
        mfcc = librosa.feature.mfcc(y=np.zeros(32), sr=22050)
    else:
        y, sr = librosa.load(audio + ".wav")
        # print(dtype)
        # print(y.size, sr, librosa.get_duration(y=y, sr=sr))
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
    return mfcc

def compare(source, target):
    source_mfcc = MFCC(source)
    target_mfcc = MFCC(target)
    dist, cost, acc_cost, path = dtw.dtw(source_mfcc.T, target_mfcc.T, dist=lambda x, y: norm(x - y, ord=1))
    print()
    print(dist)
    blank_mfcc = MFCC("blank")
    # print(blank_mfcc)
    dist1, cost, acc_cost, path = dtw.dtw(blank_mfcc.T, source_mfcc.T, dist=lambda x, y: norm(x - y, ord=1))
    print(dist1)
    print("Percent:", 1-dist/dist1)


def calculate_fingerprint(filename):
    fpcalc_out = str(subprocess.check_output(["fpcalc", "-raw", filename]))
    print(fpcalc_out)
    fingerprint_index = fpcalc_out.find("FINGERPRINT=") + 12
    fingerprints = list(map(int, fpcalc_out[fingerprint_index:-3].split(",")))

    return fingerprints

    # fpcalc_out = acoustid.fingerprint_file(filename)
    # # print(fpcalc_out)
    # fingerprints = list(map(int, fpcalc_out[1]))
    # # print(fingerprints)
    # return fingerprints

def correlation(listx, listy):
    if len(listx) == 0 or len(listy) == 0:
        # Error checking in main program should prevent us from ever being
        # able to get here.
        raise Exception('Empty lists cannot be correlated.')
    if len(listx) > len(listy):
        listx = listx[:len(listy)]
    elif len(listx) < len(listy):
        listy = listy[:len(listx)]
    covariance = 0
    for i in range(len(listx)):
        covariance += 32 - bin(listx[i] ^ listy[i]).count("1")
    covariance = covariance / float(len(listx))

    return covariance / 32

def remove_silence(sound):
    start_trim = detect_leading_silence(sound)
    print(start_trim)
    end_trim = detect_leading_silence(sound.reverse())
    print(end_trim)

    duration = len(sound)
    trimmed_sound = sound[start_trim:duration-end_trim]
    return trimmed_sound

def detect_leading_silence(sound, silence_threshold=-15.0, chunk_size=10):
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms - 400 if trim_ms - 400 >= 0 else 0

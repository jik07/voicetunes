import playsound
import sounddevice as sd
import wavio

def record_audio(duration):
    fs = 44100
    audio = sd.rec(int(fs * duration), samplerate = fs, channels = 2)
    sd.wait()
    wavio.write("recording.wav", audio, fs, sampwidth = 2)
    speak_audio("recording.wav")

def speak_audio(audio):
    playsound.playsound(audio)

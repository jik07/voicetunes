import playsound
import sounddevice as sd
import wavio
from pydub import AudioSegment

def record_audio(duration):
    print("recording")
    fs = 44100
    audio = sd.rec(int(fs * duration), samplerate = fs, channels = 2)
    sd.wait()
    wavio.write("recording.wav", audio, fs, sampwidth = 2)
    audio = AudioSegment.from_wav("recording.wav")
    trimmed_audio = remove_silence(audio)
    trimmed_audio.export("recording.wav", format="wav")
    print("started playing")
    speak_audio("recording.wav")

def speak_audio(audio):
    playsound.playsound(audio)

def remove_silence(sound):
    start_trim = detect_leading_silence(sound)
    print(start_trim)
    end_trim = detect_leading_silence(sound.reverse())

    duration = len(sound)
    trimmed_sound = sound[start_trim:duration-end_trim]
    return trimmed_sound

def detect_leading_silence(sound, silence_threshold=-15.0, chunk_size=10):
    trim_ms = 0 # ms

    assert chunk_size > 0 # to avoid infinite loop
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms - 400 if trim_ms - 400 >= 0 else 0

import audio

if __name__ == "__main__":
    # audio.record_audio("apple", 3)
    # audio.record_audio("glassisgood", 3)
    # audio.record_audio("banana", 3)
    # audio.record_audio("recording", 3)


    # audio.stretch_audio("recording", 10)

    # audio.speak_audio("apple")
    # audio.speak_audio("glassisgood")
    # audio.speak_audio("banana")
    # audio.speak_audio("recording")

    # audio.MFCC("apple")
    # audio.MFCC("recording")
    print(audio.compare("python1.wav", "python2.wav"))
    print(audio.compare("front1.wav", "front2.wav"))
    print(audio.compare("back1.wav", "back2.wav"))
    print(audio.compare("hack1.wav", "hack2.wav"))
    print(audio.compare("java1.wav", "java2.wav"))
    print(audio.compare("html1.wav", "html2.wav"))
    # audio.compare("banana", "recording")

    # print(audio.calculate_fingerprint("apple.wav"))
    # print(audio.calculate_fingerprint("recording.wav"))

    # print(audio.correlation(audio.calculate_fingerprint("apple.wav"), audio.calculate_fingerprint("recording.wav")))
    # print(audio.correlation(audio.calculate_fingerprint("Tokyo.mp3"), audio.calculate_fingerprint("Tokyo.mp3")))

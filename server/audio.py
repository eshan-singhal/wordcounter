# Messing around with the pyaudio

import json
import speech_recognition as sr

r = sr.Recognizer()

for idx, micname in enumerate(sr.Microphone.list_microphone_names()):
    if "HD USB Camera" in micname:
        mic = sr.Microphone(device_index=idx)
        break
else:
    mic = sr.Microphone(device_index=idx)


def listen():
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    # Recognise the words and store them in a db
    try:
        words = r.recognize_google(audio).split()
    except sr.UnknownValueError:
        return
    except sr.RequestError:
        return

    with open("words.db", "r") as f:
        db = json.load(f)
        for word in words:
            try:
                db[word] += 1
            except KeyError:
                db[word] = 1

    with open("words.db", "w") as f:
        json.dump(db, f, indent=4)

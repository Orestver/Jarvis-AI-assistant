import pyttsx3

def create_tts_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.setProperty('volume', 1.0)
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    return engine
#function for UI integration
"""
def speak(text, jarvis_ui):  # <-- обов'язково передаємо екземпляр UI
    def tts_job():
        engine = create_tts_engine()
        jarvis_ui.startVoiceSignal.emit()
        engine.say(text)
        engine.runAndWait()
        jarvis_ui.stopVoiceSignal.emit()
    threading.Thread(target=tts_job, daemon=True).start()
"""
def speak(text, jarvis_ui):
    engine = create_tts_engine()
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    speak('Good afternoon boss!', None)
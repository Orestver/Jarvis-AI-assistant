
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os
from playsound import playsound
from speaker import speak

load_dotenv()


elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)


def speak(txt,ui_window=None):
    try:
        audio_stream = elevenlabs.text_to_speech.convert(
            text=txt,
            voice_id="RKCbSROXui75bk1SVpy8",
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        audio_bytes = b"".join(audio_stream)
        with open("output.mp3", "wb") as f:
            f.write(audio_bytes)
        playsound("output.mp3")
        os.remove('output.mp3')
    except Exception as e:
        speak(txt,ui_window=None)





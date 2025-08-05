from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
import os

load_dotenv()
elevenlabs = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)
def speak(txt,filename):
    audio_stream = elevenlabs.text_to_speech.convert(
        text=txt,
        voice_id="RKCbSROXui75bk1SVpy8", #U4IxWQ3B5B0suleGgLcn - для віри, #wDsJlOXPqcvIUKdLXjDs - для джарвіса
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_bytes = b"".join(audio_stream)
    with open(filename, "wb") as f:
        f.write(audio_bytes)
   
os.makedirs("Jarvis_voice_commands/command_responses", exist_ok=True)

standart_responses = [
    "Closing the browser."
]

for i, phrase in enumerate(standart_responses):
    filename = f"Jarvis_voice_commands/command_responses/{phrase}.mp3"
    speak(phrase, filename)

import os
from groq import Groq
from dotenv import load_dotenv
 
load_dotenv()

# ============================================================
# Transcribe audio file using Groq Whisper v3 Turbo
# ============================================================
def transcribe_audio(audio_file) -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
 
    # If audio_file is a path string
    if isinstance(audio_file, str):
        with open(audio_file, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-large-v3-turbo",
                file=f,
                response_format="text"
            )
    else:
        # If audio_file is a file-like object (from Streamlit)
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=audio_file,
            response_format="text"
        )
 
    return transcription.strip()



# # ============================================================
# # Test
# # ============================================================
# if __name__ == "__main__":
#     import sys

#     if len(sys.argv) < 2:
#         print("Usage: python voice.py <audio_file_path>")
#         print("Example: python voice.py test.wav")
#     else:
#         audio_path = sys.argv[1]
#         print(f"Transcribing: {audio_path}")
#         result = transcribe_audio(audio_path)
#         print(f"Transcription: {result}")
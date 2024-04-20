from io import BytesIO
import os
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
from prompts import prompt, prompt_filter, sysprompt, ANSWER_PATTERN, MARKDOWN_PATTERN
from chatgpt import complete
import re
from pydub import AudioSegment

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# read in /Users/danielgeorge/Documents/work/ml/small-stuff/doctor-voice-notes/api/1713590705527.webm

file = '/Users/danielgeorge/Documents/work/ml/small-stuff/doctor-voice-notes/api/1713590705527.webm'

# Load the audio file with PyDub

# Load the audio file with PyDub
# audio = AudioSegment.from_file(BytesIO(audio_data), format="wav")


def transcribe_audio(audio_file_path: str):
    with open(audio_file_path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file)
    return transcription.text


# Transcribe the audio
transcript = transcribe_audio(file)

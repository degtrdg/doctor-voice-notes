from io import BytesIO
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from openai import OpenAI
from pydantic import BaseModel
from diff_match_patch import diff_match_patch
from typing import Any, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from .prompts import prompt, sysprompt, ANSWER_PATTERN, MARKDOWN_PATTERN
from .chatgpt import complete
import re
from pydub import AudioSegment

sessions = {}

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

# Define the request and response models


class TranscriptionRequest(BaseModel):
    audio_url: str


class TranscriptionResponse(BaseModel):
    transcript: str


class RequestBody(BaseModel):
    paragraph: str
    weakness: str


class ResponseBody(BaseModel):
    original: str
    revised: str
    diff_html: str


class ResponseModel(BaseModel):
    success: bool
    message: str | Dict[str, Any]


UPLOAD_DIRECTORY = Path(__file__).parent / "uploads"
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Whisper Transcription Service"}


class UploadRequest(BaseModel):
    session_id: str
    file: UploadFile = File(...)


@app.post("/api/upload_audio")
async def upload_audio(request: UploadRequest):
    temp_path = UPLOAD_DIRECTORY / request.file.filename
    with temp_path.open("wb") as buffer:
        shutil.copyfileobj(request.file.file, buffer)

    mp3_path = UPLOAD_DIRECTORY / "audio.mp3"
    AudioSegment.from_file(str(temp_path)).export(str(mp3_path), format="mp3")

    with open(mp3_path, 'rb') as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file)

    Path(temp_path).unlink()
    Path(mp3_path).unlink()

    def get_markdown(prompt_text, model_version):
        response = complete(messages=[{"role": "system", "content": sysprompt},
                                      {"role": "user", "content": prompt_text}], model=model_version)
        return response

    # Attempt to extract markdown from the transcription
    real_prompt = prompt.format(transcript=transcription.text)
    markdown_content = get_markdown(real_prompt, "gpt-3.5-turbo")
    match = re.search(MARKDOWN_PATTERN, markdown_content, re.DOTALL)
    if match:
        markdown_final = match.group(1).strip()
    else:
        real_prompt = prompt.format(transcript=transcription.text)
        markdown_content = get_markdown(real_prompt, "gpt-4-turbo-preview")
        match = re.search(MARKDOWN_PATTERN, markdown_content, re.DOTALL)
        if match:
            markdown_final = match.group(1).strip()
        else:
            # If no match, log error and return the original transcription
            print("Error: Could not extract markdown from the model's response.")
            print(f'real_prompt: {real_prompt}')
            print(f'markdown_content: {markdown_content}')
            return ResponseModel(
                success=False,
                message="Could not extract markdown from the model's response."
            )

    # Update the session with the transcription text
    if request.session_id not in sessions:
        sessions[request.session_id] = {
            "diarization": [],
            "curr_checklist": [],
        }
    sessions[request.session_id]['diarization'].append(markdown_final)

    # Return the markdown content
    return ResponseModel(
        success=True,
        message={"diarization": markdown_final}
    )


@app.get("/api/all_transcripts/{session_id}")
def get_total_transcript(session_id: str):
    # might be a problem if context length is too long but fine for now
    total_diarization = sessions[session_id]['diarization'].join('\n')
    return ResponseModel(
        success=True,
        message={"diarization": total_diarization}
    )


@app.get("/api/checklist/{session_id}")
def get_checklist(session_id: str):
    # might be a problem if context length is too long but fine for now
    total_diarization = sessions[session_id]['diarization'].join('\n')

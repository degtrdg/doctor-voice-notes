from io import BytesIO
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from openai import OpenAI
from pydantic import BaseModel
from typing import Any, Dict, Optional
from fastapi.middleware.cors import CORSMiddleware
from prompts import prompt, sysprompt, MARKDOWN_PATTERN
from chatgpt import complete
import modal
import traceback
# from prompts import prompt, sysprompt, MARKDOWN_PATTERN
# from chatgpt import complete
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


web_app = FastAPI(docs_url="/api/docs", openapi_url="/api/openapi.json")

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


image = (
    modal.Image.debian_slim(python_version="3.11")
    .env({"OPENAI_API_KEY": ""})
    .run_commands(
        "python3 --version",
        "apt-get update",
        "apt-get install -y git",
        # "apt-get install -y wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev",
        # "apt-get update && apt-get install ffmpeg libsm6 libxext6  -y",
        "apt-get update && apt-get install ffmpeg -y",
        # "pip3 install --upgrade setuptools wheel cmake",
    )
    .pip_install_from_requirements("requirements.txt")
)

app = modal.App("doctor-voice-app")


# stub = modal.Stub(name="doctor-voice", image=image)
sessions = modal.Dict.from_name("my-dict", create_if_missing=True)
# stub.user_video_data = modal.Dict.new()

@web_app.get("/")
async def root():
    return {"message": "Whisper Transcription Service"}


@web_app.post("/api/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    try:
        print('Received upload request:', file)
        print('func')
        temp_path = UPLOAD_DIRECTORY / file.filename
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        mp3_path = UPLOAD_DIRECTORY / "audio.mp3"
        AudioSegment.from_file(str(temp_path)).export(
            str(mp3_path), format="mp3")

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
                # print("Error: Could not extract markdown from the model's response.")
                print(f'real_prompt: {real_prompt}')
                # print(f'markdown_content: {markdown_content}')
                return ResponseModel(
                    success=False,
                    message="Could not extract markdown from the model's response."
                )

        # Update the session with the transcription text
        if not sessions.contains(sessions):
            sessions['1'] = {
                "diarization": [],
                "curr_checklist": [],
            }
        print(f'markdown {markdown_final}')
        sessions['1']['diarization'].append(markdown_final)

        # Return the markdown content
        return ResponseModel(
            success=True,
            message={"diarization": markdown_final}
        )

    except Exception as e:
        print(e)
        return ResponseModel(
            success=False,
            message=f"An error occurred during transcription. {e} {traceback.format_exc()}"
        )


@web_app.get("/api/all_transcripts/{session_id}")
def get_total_transcript(session_id: str):
    # might be a problem if context length is too long but fine for now
    # total_diarization = sessions[session_id]['diarization'].join('\n')

    example = """
Doctor: Hello Mr. George, how are you today?
Patient: Hello Doctor, I feel a lot more tired than usual and I've been unintentionally losing a lot of weight- I'm a lot skinnier now.
Doctor: Oh I see, let's get to the bottom of this. Are you experiencing any of the following: frequent urination, blurred vision, or poor wound healing?
Patient: Hm, I think I have been experiencing frequent urination and blurred vision.
Doctor: It seems like you have Type 2 Diabetes. I am going to prescribe you metformin. Are you on any other medication?
Patient: No I am not. **_checks off Not On Other Medication_**
Doctor: Okay. Have you ever had an infection in your liver or kidneys?
Patient: No, I have not had any. **_checks off Must Not Have Liver Disease or Kidney Disease_**
Doctor: Perfect. Are you allergic to any medication?
Patient: No. **_checks off Must Not Be Allergic to Metformin_**
""".strip()

    return ResponseModel(
        success=True,
        message={"diarization": example}
    )


@web_app.get("/api/checklist/{session_id}")
def get_checklist(session_id: str):
    # might be a problem if context length is too long but fine for now
    total_diarization = sessions[session_id]['diarization'].join('\n')


@app.function(image=image)
@modal.asgi_app()
def fastapi_app():
    return web_app
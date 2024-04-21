from io import BytesIO
import json
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, WebSocket
from openai import OpenAI
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from fastapi.middleware.cors import CORSMiddleware
from prompts import (
    prompt,
    sysprompt,
    MARKDOWN_PATTERN,
    prompt_extract_drug,
    JSON_PATTERN,
    prompt_checklist,
    sysprompt_checklist,
    sysprompt_extract_drug,
    drugs,
    prompt_fix_diarization,
    sysprompt_fix_diarization
)
from chatgpt import complete

# from prompts import prompt, sysprompt, MARKDOWN_PATTERN, prompt_extract_drug, JSON_PATTERN, prompt_checklist, sysprompt_checklist, sysprompt_extract_drug, drugs
# from chatgpt import complete
import re
from pydub import AudioSegment

import modal

from firebase_provider import (
    get_sessions_db,
    append_to_transcript,
    get_checklist,
    get_transcript,
    add_drug,
    get_drugs,
    set_checklist,
    create_session,
    set_transcription
)

sessions = get_sessions_db()

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


class ChecklistModel(BaseModel):
    success: bool
    checklist: Any


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

# mounts = [
#     modal.Mount.from_local_file(
#         "doctor-voice-notes-firebase-adminsdk-3xtos-a8c7dc1ead.json",
#         "/doctor-voice-notes-firebase-adminsdk-3xtos-a8c7dc1ead.json",
#     )
# ]

image = (
    modal.Image.debian_slim(python_version="3.11")
    .env({"OPENAI_API_KEY": "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"})
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

app = modal.App("doctor-voice-app-2")


@web_app.get("/")
async def root():
    return {"message": "Whisper Transcription Service"}


@web_app.get("/api/initialize_session")
async def initialize_session(session_id: str):
    all_sessions_data = get_sessions_db()
    if session_id not in all_sessions_data:
        import time
        name = time.strftime("%H:%M %m-%d-%Y", time.localtime())
        create_session(session_id, name)
    return ResponseModel(success=True, message="Session initialized")


@web_app.post("/api/upload_audio")
async def upload_audio(file: UploadFile = File(...), session_id: str = Form()):
    try:
        print("Received upload request:", file)
        print("func")
        temp_path = UPLOAD_DIRECTORY / file.filename
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        mp3_path = UPLOAD_DIRECTORY / "audio.mp3"
        AudioSegment.from_file(str(temp_path)).export(str(mp3_path), format="mp3")

        with open(mp3_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt="Omeprazole, Medical Marijuana, Acetaminophen, Warfarin, Metformin, Albuterol, Sertraline",
            )
        Path(temp_path).unlink()
        Path(mp3_path).unlink()

        def get_markdown(prompt_text, model_version):
            response = complete(
                messages=[
                    {"role": "system", "content": sysprompt},
                    {"role": "user", "content": prompt_text},
                ],
                model=model_version,
            )
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
                print(f"real_prompt: {real_prompt}")
                # print(f'markdown_content: {markdown_content}')
                return ResponseModel(
                    success=False,
                    message="Could not extract markdown from the model's response.",
                )

        # if the session does not exist, create it
        all_sessions_data = get_sessions_db()
        if session_id not in all_sessions_data:
            import time
            # name is time in HH:MM MM-DD-YYYY format
            name = time.strftime("%H:%M %m-%d-%Y", time.localtime())
            create_session(session_id, name)


        # Update the session with the transcription text
        # if session_id not in sessions:
        #     pass
        # sessions['1'] = {
        #     "diarization": [],
        #     "curr_checklist": [],
        # }
        print(f"markdown {markdown_final}")

        for transcript_line in markdown_final.split("\n"):
            role, text = transcript_line.split(": ", 1)
            append_to_transcript(session_id, text, role)

        # sessions['1']['diarization'].append(markdown_final)
        get_drugs_list_update_firebase(session_id)
        get_checklist_state(session_id)

        if len(get_checklist(session_id).keys()) % 6 == 0:
            fix_diarization(session_id)

        # Return the markdown content
        return ResponseModel(success=True, message={"diarization": markdown_final})

    except Exception as e:
        print(e)
        return ResponseModel(
            success=False, message=f"An error occurred during transcription. {e}"
        )


def complete_helper(prompt_text, sysprompt, model_version, use_cache=True):
    response = complete(
        messages=[
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": prompt_text},
        ],
        model=model_version,
        use_cache=use_cache,
    )
    return response


def fix_diarization(session_id: str):
    all_sessions_data = get_sessions_db()
    if session_id not in all_sessions_data:
        raise HTTPException(status_code=404, detail="Session not found")
    # Join all transcripts in the session
    # Retrieve the session data
    transcript = get_transcript(session_id)
    # Turn transcriptions into str
    full_transcript = "\n".join(
        [f"{entry['user']}: {entry['text']}" for entry in transcript]
    )
    curr_prompt = prompt_fix_diarization.format(transcript=full_transcript)
    response = complete_helper(curr_prompt, sysprompt_fix_diarization, 'gpt-4-turbo')
    match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
    if match:
        new_transcript = match.group(1).strip()
    else:
        response = complete_helper(
            curr_prompt, sysprompt_extract_drug, "gpt-4-turbo", use_cache=False)
        match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
        if match:
            new_transcript = match.group(1).strip()


        else:
            print(
                "Error: Could not extract md block from the model's response.")
            return []
        
    # process the new_transcript and put it up
    total_transcript = {}
    for idx, transcript_line in enumerate(new_transcript.split("\n")):
        role, text = transcript_line.split(": ", 1)
        total_transcript[f"wuggy{idx}"] = {'text': text, 'user': role}

    set_transcription(session_id, total_transcript)
        
    return transcript

    

def get_checklist_state(session_id: str) -> list: # async
    all_sessions_data = get_sessions_db()
    if session_id not in all_sessions_data:
        raise HTTPException(status_code=404, detail="Session not found")

    # Join all transcripts in the session
    # Retrieve the session data
    transcript = get_transcript(session_id)

    # Join all transcripts in the session
    full_transcript = "\n".join(
        [f"{entry['user']}: {entry['text']}" for entry in transcript]
    )
    assert full_transcript not in [None, ""], "Transcript is empty"

    drugs_list = get_drugs(session_id)
    drug_checklist = []
    # Get a checklist from the drugs
    for drug in drugs_list:
        if drug in drugs:
            drug_checklist.append(drugs[drug]['contraindications'])

    checklist_state = [[
        {
            "description": "Doctor asked patient for current medications",
            "checked": False
        },
        {
            "description": "Doctor asked patient for current symptoms",
            "checked": False
        },
        {
            "description": "Doctor gave diagnosis or verdict on ailment",
            "checked": False
        },
        {
            "description": "Doctor prescrived medication to patient",
            "checked": False
        }
    ]] + drug_checklist

    # If there is a checklist, update it based on the transcript
    curr_prompt = prompt_checklist.format(checklist=json.dumps(checklist_state, indent=2), transcript=full_transcript)
    response = complete_helper(curr_prompt, sysprompt_checklist, "gpt-4-turbo")
    match = re.search(JSON_PATTERN, response, re.DOTALL)
    if match:
        # TODO: this needs more checks but should be fine tbh
        updated_checklist = json.loads(match.group(1).strip())
        # updated_checklist = [item for sublist in updated_checklist for item in sublist]
        print(updated_checklist)
        # update firebase
        final_checklist_dict = {}

        for idx, checklist_drug_group in enumerate(updated_checklist):
            for i, item in enumerate(checklist_drug_group):
                final_checklist_dict[str(idx*10 + i)] = {
                    "text": item["description"],
                    "checked": item["checked"],
                    "word_relation": str(idx)
                }

        set_checklist(session_id, final_checklist_dict)

        return updated_checklist
    else:
        # If the checklist cannot be updated, return the current state with an error message
        print(
            "Error: Could not extract the updated checklist from the model's response.")
        checklist_state = {
            "message": "Could not update the checklist based on the transcript."}
        return []

def get_drugs_list_update_firebase(session_id: str) -> list: # async
    all_sessions_data = get_sessions_db()
    if session_id not in all_sessions_data:
        raise HTTPException(status_code=404, detail="Session not found")

    # Join all transcripts in the session
    # Retrieve the session data
    transcript = get_transcript(session_id)

    # Join all transcripts in the session
    full_transcript = "\n".join(
        [f"{entry['user']}: {entry['text']}" for entry in transcript]
    )
    assert full_transcript not in [None, ""], "Transcript is empty"

    curr_prompt = prompt_extract_drug.format(transcript=full_transcript)
    response = complete_helper(curr_prompt, sysprompt_extract_drug, "gpt-3.5-turbo")
    match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
    if match:
        drugs_list = match.group(1).strip()
    else:
        response = complete_helper(
            curr_prompt, sysprompt_extract_drug, "gpt-3.5-turbo", use_cache=False)
        match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
        if match:
            drugs_list = match.group(1).strip()
        else:
            print(
                "Error: Could not extract md block from the model's response.")
            return []

    drugs_list = drugs_list.strip().split('\n')
    cur_drug_list = get_drugs(session_id)

    for drug in drugs_list:
        if drug and drug not in cur_drug_list:
            add_drug(session_id, drug)
    return drugs_list


@app.function(image=image) # , mounts=mounts
@modal.asgi_app()
def fastapi_app():
    return web_app

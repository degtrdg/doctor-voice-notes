from io import BytesIO
import json
import os
from pathlib import Path
import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile, WebSocket
from openai import OpenAI
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from fastapi.middleware.cors import CORSMiddleware
from .prompts import prompt, sysprompt, MARKDOWN_PATTERN, prompt_extract_drug, JSON_PATTERN, prompt_checklist, sysprompt_checklist, sysprompt_extract_drug, drugs
from .chatgpt import complete
# from prompts import prompt, sysprompt, MARKDOWN_PATTERN, prompt_extract_drug, JSON_PATTERN, prompt_checklist, sysprompt_checklist, sysprompt_extract_drug, drugs
# from chatgpt import complete
import re
from pydub import AudioSegment

sessions = {
    "1": {
        "diarization": [
            """
Doctor: Hello Mr. George, how are you today?
Patient: Hello Doctor, I feel a lot more tired than usual and I've been unintentionally losing a lot of weight- I'm a lot skinnier now.
Doctor: Oh I see, let's get to the bottom of this. Are you experiencing any of the following: frequent urination, blurred vision, or poor wound healing?
Patient: Hm, I think I have been experiencing frequent urination and blurred vision.
Doctor: It seems like you have Type 2 Diabetes. I am going to prescribe you metformin. Are you on any other medication?
Patient: No I am not.
Doctor: Okay. Have you ever had an infection in your liver or kidneys?
Patient: No, I have not had any.
Doctor: Perfect. Are you allergic to any medication?
Patient: No.
""".strip()
        ],
        "curr_checklist": [],
        'drug': 'Metformin'
    }
}

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


@app.post("/api/upload_audio")
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
                model="whisper-1", file=audio_file, prompt="Omeprazole, Medical Marijuana, Acetaminophen, Warfarin, Metformin, Albuterol, Sertraline")
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
        if '1' not in sessions:
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
            message=f"An error occurred during transcription. {e}"
        )


@app.get("/api/all_transcripts/{session_id}")
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


def get_checklist(prompt_text, model_version, use_cache=True):
    response = complete(messages=[{"role": "system", "content": sysprompt},
                                  {"role": "user", "content": prompt_text}], model=model_version, use_cache=use_cache)
    return response


@app.get("/api/checklist_state/{session_id}")
async def get_checklist_state(session_id: str):
    # Retrieve the session data
    session_data = sessions.get(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    # Join all transcripts in the session
    full_transcript = '\n'.join(session_data.get('diarization', []))
    assert session_data.get('diarization', []) != []
    drug = session_data.get('drug', [])

    # If there is a checklist, update it based on the transcript
    checklist_flat = sessions['curr_checklist']
    curr_prompt = prompt_checklist.format(
        drug=drug, checklist=json.dumps(checklist_flat, indent=2), transcript=full_transcript)
    response = get_checklist(curr_prompt, "gpt-4-turbo")
    match = re.search(JSON_PATTERN, response, re.DOTALL)
    if match:
        # TODO: this needs more checks but should be fine tbh
        updated_checklist = json.loads(match.group(1).strip())
        checklist_state['contraindications'] = updated_checklist
    else:
        # If the checklist cannot be updated, return the current state with an error message
        print(
            "Error: Could not extract the updated checklist from the model's response.")
        checklist_state = {
            "message": "Could not update the checklist based on the transcript."}
        return ChecklistModel(
            success=False,
            checklist=checklist_state
        )

    return ChecklistModel(
        success=True,
        checklist=updated_checklist
    )


@app.get("/api/drug_list/{session_id}")
async def get_drugs_list(session_id: str):
    # Retrieve the session data
    session_data = sessions.get(session_id)
    if not session_data:
        raise HTTPException(status_code=404, detail="Session not found")

    # Join all transcripts in the session
    full_transcript = '\n'.join(session_data.get('diarization', []))
    assert session_data.get('diarization', []) != []

    # Initialize the checklist state
    checklist_state = session_data.get('curr_checklist')

    curr_prompt = prompt_extract_drug.format(transcript=full_transcript)
    response = get_checklist(curr_prompt, "gpt-3.5-turbo")
    match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
    if match:
        drug = match.group(1).strip()
    else:
        response = get_checklist(
            curr_prompt, "gpt-3.5-turbo", use_cache=False)
        drug = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
        if match:
            drugs_list = match.group(1).strip()
        else:
            print(
                "Error: Could not extract md block from the model's response.")
            # If no checklist is found, return an empty checklist state
            checklist_state = {
                "message": "Could not extract md block from the model's response."}
            return ChecklistModel(
                success=False,
                checklist=checklist_state
            )

        drugs_list = drug.strip().split('\n')
        checklist_state = []

        if not drugs_list:
            return ChecklistModel(
                success=True,
                checklist={}
            )

        for drug in drugs_list:
            if drug in drugs:
                checklist_state.append(drugs[drug]['contraindications'])

    return ChecklistModel(
        success=True,
        checklist=checklist_state
    )

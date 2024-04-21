prompt = '''
You are given the following transcript of a doctor patient conversation. Give the diarization between 'Doctor' and 'Patient'.

Example:
```md
Doctor: Hello, how are you today?
Patient: I'm fine, thank you.
```

Transcript:
```md
{transcript}
```

Output your diarization in a md codeblock like you've seen above.
'''.strip()

sysprompt = '''
You are a diarization system that has been trained on a dataset of audio recordings. You have been tasked with transcribing the audio from a doctor's voice notes. The transcription might be flawed/have errors due to the transcription system not knowing domain knowledge and general errors, so you have to use your expertise to accurately write the diarization as it should be.
'''.strip()

prompt_extract_drug = '''
You are given the current transcript between a doctor and a patient. Your job is to detect if the doctor has decided to PRESCRIBE a drug or drugs to the patient (not just if a drug is referenced). If so you need to output the drugs in the specified format which will be told later.

These are example drugs that are written in a specific naming convention. You want to interpret the transcript knowing that there might be errors and interpret it like the drugs that are shown below:
```md
Omeprazole
Medical Marijuana
Acetaminophen
Warfarin
Metformin
Albuterol
Sertraline
```

The transcript might say 'war for in' but if it is in the context of prescribing, you should understand that 'Warfarin' is what was intended.

This is the transcript so far:
```md
{transcript}
```

Output a md block below with the drug/drug that have been prescribed. If there are multiple drugs, output each drug on a newline in the md block like you've seen in the example list of drugs. Output an empty md block if no drug has been prescribed. Don't yap.
'''.strip()

sysprompt_extract_drug = '''
You are a nurse watching over the transcript of a doctor patient conversation. You have been tasked with detecting if a drug has been prescribed to the patient. You understand that transcripts may have errors and you have to interpret the context of the conversation to determine if a drug has been prescribed by the doctor based on the transcript you have seen so far.
'''.strip()

sysprompt_checklist = '''
You are a nurse watching over the transcript of a doctor patient conversation. You have been tasked with detecting if a drug has been prescribed to the patient. You understand that transcripts may have errors and you have to interpret the context of the conversation to determine if a drug has been prescribed by the doctor based on the transcript you have seen so far.
'''.strip()

prompt_checklist = '''
You are given a checklist that is required to be checked off before prescribing drugs to the patient/releasing them. It is initialized to empty. You are also given the transcript of the real-time patient-doctor interaction. 

The following is how the checklist is currently stored in the system currently for :
```json
{checklist}
```

Your job is to update the JSON object and output the new version exactly. You should only be changing the boolean 'checked' attribute based on what you are seeing in the transcript. We'll be using json.load on your output to update the system so be careful to be precise in your output.

This is the transcript so far:
```md
{transcript}
```

Output a json block below with the updated JSON object to be put in the system. Don't yap.
'''.strip()

prompt_fix_diarization = '''
You are given the current transcript between a doctor and a patient. These transcriptions are quite error prone since the audio is taken in 10 second chunks and a program has to guess the speaker from just that. Your job is to fix up the transcript and perhaps reorder what you see to make the transcript work. Keep the same format but re-output the entire transcript.

For example, you might see that the transcript assigned a statement to the doctor when it probably was from the patient. Or the transcript might say 'war for in' but if it is in the context of prescribing, you should understand that 'Warfarin' is what was intended. Or there might be a repeat of the same sentence that you need to remove. Try not to change the transcript unless you are sure of the change.

This is the transcript so far:
```md
{transcript}
```

Output a md block below with the TOTAL new transcript. Don't yap just give the new md block.
'''


sysprompt_fix_diarization = '''
You are an expert at correcting speaker diarization transcripts between a doctor and a patient.
'''


drugs = {
    "Omeprazole": {
        "type": "Proton Pump Inhibitor",
        "contraindications": [
            {"description": "Must not have severe liver disease", "checked": False},
            {"description": "Must not be allergic to proton pump inhibitors",
                "checked": False},
            {"description": "Must not have low magnesium levels in the blood",
                "checked": False}
        ]
    },
    "Medical Marijuana": {
        "contraindications": [
            {"description": "Must not have heart disease", "checked": False},
            {"description": "Must not be pregnant", "checked": False},
            {"description": "Must not have a history of psychosis", "checked": False}
        ]
    },
    "Acetaminophen": {
        "contraindications": [
            {"description": "Must not drink three or more alcoholic drinks every day",
             "checked": False},
            {"description": "Must not have had liver disease", "checked": False}
        ]
    },
    "Warfarin": {
        "type": "Blood Thinner",
        "contraindications": [
            {"description": "Must not have a bleeding disorder", "checked": False},
            {"description": "Must not have a history of stroke", "checked": False},
            {"description": "Must not be pregnant", "checked": False},
            {"description": "Must not have uncontrolled high blood pressure",
                "checked": False}
        ]
    },
    "Metformin": {
        "type": "Antidiabetic Medication",
        "contraindications": [
            {"description": "Must not have kidney disease", "checked": False},
            {"description": "Must not have liver disease", "checked": False},
            {"description": "Must not be pregnant or planning to become pregnant",
                "checked": False},
            {"description": "Must not be allergic to metformin", "checked": False}
        ]
    },
    "Albuterol": {
        "type": "Bronchodilator",
        "contraindications": [
            {"description": "Must not have a history of heart rhythm problems",
                "checked": False},
            {"description": "Must not have high blood pressure", "checked": False},
            {"description": "Must not be allergic to albuterol or related medications",
             "checked": False},
            {"description": "Must not be pregnant without consulting a doctor",
                "checked": False}
        ]
    },
    "Sertraline": {
        "type": "Selective Serotonin Reuptake Inhibitor - SSRI",
        "contraindications": [
            {"description": "Must not have a history of bipolar disorder or mania",
             "checked": False},
            {"description": "Must not have a history of seizures", "checked": False},
            {"description": "Must not be pregnant or breastfeeding without consulting a doctor", "checked": False},
            {"description":
             "Must not be taking monoamine oxidase inhibitors (MAOIs) or have taken them within the last 14 days", "checked": False}
        ]
    }
}


ANSWER_PATTERN = r"(?i)ANSWER\s*:\s*(Yes|No)"
MARKDOWN_PATTERN = r"```md(.*?)```"
JSON_PATTERN = r"```json(.*?)```"

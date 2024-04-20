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
You are given the current transcript between a doctor and a patient. Your job is to detect if the doctor has decided to PRESCRIBE a drug to the patient (not just if a drug is referenced). If so you need to output the drug in the specified format which will be told later.

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

Output a md block below with the drug that has been prescribed. Output an empty md block if no drug has been prescribed. Don't yap.
'''.strip()

sysprompt_extract_drug = '''
You are a nurse watching over the transcript of a doctor patient conversation. You have been tasked with detecting if a drug has been prescribed to the patient. You understand that transcripts may have errors and you have to interpret the context of the conversation to determine if a drug has been prescribed by the doctor based on the transcript you have seen so far.
'''.strip()

sysprompt_checklist = '''
You are a nurse watching over the transcript of a doctor patient conversation. You have been tasked with detecting if a drug has been prescribed to the patient. You understand that transcripts may have errors and you have to interpret the context of the conversation to determine if a drug has been prescribed by the doctor based on the transcript you have seen so far.
'''.strip()

prompt_checklist = '''
You are given a checklist that is required to be checked off before prescribing {drug}. You are also given the transcript of the real-time patient-doctor interaction. 

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

ANSWER_PATTERN = r"(?i)ANSWER\s*:\s*(Yes|No)"
MARKDOWN_PATTERN = r"```md(.*?)```"
JSON_PATTERN = r"```json(.*?)```"

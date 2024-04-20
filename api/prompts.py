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

ANSWER_PATTERN = r"(?i)ANSWER\s*:\s*(Yes|No)"

MARKDOWN_PATTERN = r"```md(.*?)```"

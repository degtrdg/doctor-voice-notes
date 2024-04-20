import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('doctor-voice-notes-firebase-adminsdk-3xtos-a8c7dc1ead.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://doctor-voice-notes-default-rtdb.firebaseio.com/'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('Session')
# print(ref.get())

# append to checklist, 
def append_to_checklist(session_id: str, text: str, word_relation: str, checked: bool):
    ref = db.reference('Session/' + session_id + '/Checklist')
    ref.push({
        'text': text,
        'word_relation': word_relation,
        'checked': checked
    })

# session_id, text, user
def append_to_transcript(session_id: str, text: str, user: str):
    ref = db.reference('Session/' + session_id + '/Transcript')
    ref.push({
        'text': text,
        'user': user
    })

# 
def get_sessions_db():
    ref = db.reference('Session')
    return ref.get()

def get_checklist(session_id: str):
    ref = db.reference('Session/' + session_id)
    if "Checklist" not in ref.get():
        return {}
    ref = db.reference('Session/' + session_id + '/Checklist')
    return ref.get()

def get_transcript(session_id: str):
    ref = db.reference('Session/' + session_id)
    if "Transcript" not in ref.get():
        return {}
    ref = db.reference('Session/' + session_id + '/Transcript')
    return ref.get()

def add_drug(session_id: str, drug: str):
    ref = db.reference('Session/' + session_id + '/Drugs')
    ref.push(drug)

# append_to_checklist('1', 'Toggle Prolenu', 'Doctor', False)
# append_to_transcript('1', 'as;doifjaisdufnau naosdhf oashdf oahsdfoasodf ioasjf ioasjf dsaf ', 'Doctor')
# add_drug('1', 'Metformin')

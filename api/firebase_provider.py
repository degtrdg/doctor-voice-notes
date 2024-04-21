import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
credential = {
  "type": "service_account",
  "project_id": "doctor-voice-notes",
  "private_key_id": "a8c7dc1ead30d500ab7055fcb52c5fd3a32eaa51",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC8kOImSuBwODDg\nBYQWHJs9jU4sj3gDHQaCKLGfNsGeZESF4jYgIflBEl8i/x8FmIzFCv9aB9wUs+cB\nG/2K8WAkt1M51ovdN9UCIFcJjryNv+7nzGUoEzZwFtMHLsJOSJT+ZmujYYiJbrh8\n7JpIICQ4vsapWUFGqeu4uRHZvvKwk06HNiAahdV1K23p8aOQiTPWpLwma0Z97Zp/\nghOTM4Pt9rNSiJtjdLeQVtCuFt86TNGNLNGBSVygMwHWpyB+JxiAos/OcRQI05gN\n+0fWC8LdhDJvbksq1GBPlYzqcWfO10lNr4gK1/NNHEnoYwp26Gr4jtXqcFdhvXcz\n/DxVwEfpAgMBAAECggEACpY51DuM+U/2UoWMwm8Nujl2Q6M0cjxNcr5VJqK84Scw\n/7FRJ6GwrFobNExNkhNcB+4Toxrg3Nqy5AmNxSDDLJyMVCl7BcsOLwXgzR0R8gVu\nJN6BaWwWuNlXNMaHyzxg/R2D+pLNxyWLvxvLl7QSRItVfQmRVCXTIbZmTareVlJ+\nDOYg/iEizokGzcJQpGuy72ZREzdOFyL2PBkZ1aif673g9sikM/wIBmo+KuLY8sP0\nBI3ewk7eqrdTjWK1FoVWnf2lZ99mWbx1kjO3FsXwRxuRxeX/rbT/wVwPOXayc9pQ\nn7xb3qsk0bIWS9/k04QdoNGPmdwKT8gDFSgbrsBt2QKBgQD5wvSwD44sSvjelYVp\n6JDQlFu66nC43SolVdZmJwReyBWdRYvvhze4rDayJ4rRvBcZLMdJijqtPNetnpD1\nNt3O+QdhBxWjflKOJrl8gtrW15qpNlIGjBM/5cZwVdSDpJFEwh1bIXu3ddWloCZJ\nrxFSDQveuSQ34eaWgg/4Xe9RZQKBgQDBRqBGhgk7m4vV286KhTGoX98mEmGkPmqD\n8Xc5CngofzE4yr6clHSnnQlLAnViBLRcd8gP1P3Zi1zXSHQP2aRIAs46vE7veHZx\nJBSEAwEe4QN1/OjP7dkzuulEEAJNW8rEkVjNxCvzJYTpX1uPhyyy7ZXuJ0TOSIou\nXQdOcuLWNQKBgBaD8LL+c/6iM5U9PW2yvXtQJITRJaBEr8v11QIYelhhCTHIVzkc\no3VOcQ/WaLlHj32Bf+WtRGThmz/Xj5HLhGtoH7YrgVPfy2ltLEOBOGEtxo+Cihp0\n/jdAa4cs9Z94cnAUX7kbZ5++S6hGq6zwz0rqSiul3RH8l2DyEKZ/MVfRAoGBAIj9\nOQ6jZBnmptdeo2cU/txbj3uZnbFfN/nrBNjeLcpuVIHvWej7ZC+FI5gR1wcxVHER\nyTBHg+FUYOqKBRFS7pjHvEpvO/eJx1FsBEqJIpszW1OefZka+U8sFLfULP2NqQto\nBaxaddgx6KHMn8X8RldQBGu3U5JuYdp4v3v/+/1dAoGAF3k4DYSJ1nQTh/P6hF+P\nsYig6dytB0IED5qzwkEAhwjLA3nxTRJZyX8jrrVPPvhlV+RsF28KTLJd6J4a7XfM\nQnQxNGVW94wLmsV4jp7lcGdcpf4gBNCNp4mwHGtzcgr/92mm+rmOPdwJ73hzo+6F\ntJGkhvXOdGyVtmhszBY7WY4=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3xtos@doctor-voice-notes.iam.gserviceaccount.com",
  "client_id": "111845280188141515833",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3xtos%40doctor-voice-notes.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

import json
import traceback
# write the credential to a file
with open('doctor-voice-notes-firebase-adminsdk-3xtos-a8c7dc1ead.json', 'w') as f:
    json.dump(credential, f)

try:
    cred = credentials.Certificate('doctor-voice-notes-firebase-adminsdk-3xtos-a8c7dc1ead.json')
    print('Firebase credential loaded')
except Exception as e:
    message=f"An error occurred {e} {traceback.format_exc()}"
    print(message)

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

def set_checklist(session_id: str, checklist: dict):
    ref = db.reference('Session/' + session_id + '/Checklist')
    ref.set(checklist)

# session_id, text, user
def append_to_transcript(session_id: str, text: str, user: str):
    ref = db.reference('Session/' + session_id + '/Transcript')
    ref.push({
        'text': text,
        'user': user
    })


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
        return []
    ref = db.reference('Session/' + session_id + '/Transcript')
    return ref.get().values()

def add_drug(session_id: str, drug: str):
    ref = db.reference('Session/' + session_id + '/Drugs')
    ref.push(drug)

def set_checklist(session_id: str, checklist: dict):
    ref = db.reference('Session/' + session_id + '/Checklist')
    ref.set(checklist)

def set_transcription(session_id:str, transcriptions:dict):
    ref = db.reference('Session/' + session_id + '/Transcript')
    ref.set(transcriptions)

def get_drugs(session_id: str):
    ref = db.reference('Session/' + session_id)
    if "Drugs" not in ref.get():
        return []
    ref = db.reference('Session/' + session_id + '/Drugs')
    return ref.get().values()

def create_session(session_id: str, name: str):
    ref = db.reference('Session/' + session_id)
    ref.set({
        'name': name
    })

# append_to_checklist('1', 'Toggle Prolenu', 'Doctor', False)
# append_to_transcript('banana', 'awesome sauce banana yap yap yap yap yap yap banana yap yap yap yap yap yap', 'Doctor')
# add_drug('1', 'Metformin')

# print(get_sessions_db())
# print("two" in get_sessions_db())

# set_checklist('2', {
#     '2': {
#         'text': 'Toggle Prolenu',
#         'checked': False
#     },
#     '3': {
#         'text': 'Toggle Prolenu',
#         'checked': False
#     }
# })
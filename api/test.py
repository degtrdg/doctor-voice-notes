import json
import os
import re
from openai import OpenAI
from prompts import JSON_PATTERN, prompt, prompt_extract_drug, sysprompt_checklist, sysprompt_extract_drug, prompt_checklist, sysprompt, ANSWER_PATTERN, MARKDOWN_PATTERN
from chatgpt import complete

client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")


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

# Nothing should happen
chunk1 = """
Doctor: Hello Mr. George, how are you today?
Patient: Hello Doctor, I feel a lot more tired than usual and I've been unintentionally losing a lot of weight- I'm a lot skinnier now.
Doctor: Oh I see, let's get to the bottom of this. Are you experiencing any of the following: frequent urination, blurred vision, or poor wound healing?
""".strip()

# Checklist should appear AND the first item should be checked off
chunk2 = """
Doctor: Hello Mr. George, how are you today?
Patient: Hello Doctor, I feel a lot more tired than usual and I've been unintentionally losing a lot of weight- I'm a lot skinnier now.
Doctor: Oh I see, let's get to the bottom of this. Are you experiencing any of the following: frequent urination, blurred vision, or poor wound healing?
Patient: Hm, I think I have been experiencing frequent urination and blurred vision.
Doctor: It seems like you have Type 2 Diabetes. I am going to prescribe you metformin. Are you on any other medication?
Patient: No I am not.
Doctor: Okay. Have you ever had an infection in your liver or kidneys?
""".strip()

# Checklist should appear AND the second item should be checked off
# but not the third because that hasn't been said yet
chunk3 = """
Doctor: Hello Mr. George, how are you today?
Patient: Hello Doctor, I feel a lot more tired than usual and I've been unintentionally losing a lot of weight- I'm a lot skinnier now.
Doctor: Oh I see, let's get to the bottom of this. Are you experiencing any of the following: frequent urination, blurred vision, or poor wound healing?
Patient: Hm, I think I have been experiencing frequent urination and blurred vision.
Doctor: It seems like you have Type 2 Diabetes. I am going to prescribe you metformin. Are you on any other medication?
Patient: No I am not.
Doctor: Okay. Have you ever had an infection in your liver or kidneys?
Patient: No, I have not had any. 
Doctor: Perfect. Are you allergic to any medication?
""".strip()

# All three has been checked off
chunk3 = """
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

list_of_drugs = list(drugs.keys())


# If there isn't a checklist, you need to check for a prescription on the current transcript

checklist = None

# Function to call the complete function and extract the answer


def get_checklist(prompt_text, model_version):
    response = complete(messages=[{"role": "system", "content": sysprompt},
                                  {"role": "user", "content": prompt_text}], model=model_version)
    return response


# Getting the checklist check
if not checklist:
    curr_prompt = prompt_extract_drug.format(transcript=chunk1)
    response = get_checklist(curr_prompt, "gpt-3.5-turbo")
    print(response)
    # Extract the checklist from the response
    match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
    print(checklist)
    if match:
        checklist = match.group(1).strip()
    else:
        curr_prompt = prompt_extract_drug.format(transcript=chunk1)
        response = get_checklist(curr_prompt, "gpt-4-turbo-preview")
        drug = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
        if match:
            drug = match.group(1).strip()
        else:
            print("Error: Could not extract the checklist from the model's response.")
            drug = None

# There should be an empty drug
print('drug should be empty')
print(f'drug {drug}')

# Getting the checklist check
if not checklist:
    curr_prompt = prompt_extract_drug.format(transcript=chunk2)
    response = get_checklist(curr_prompt, "gpt-3.5-turbo")
    print(response)
    # Extract the checklist from the response
    match = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
    print(checklist)
    if match:
        checklist = match.group(1).strip()
    else:
        curr_prompt = prompt_extract_drug.format(transcript=chunk2)
        response = get_checklist(curr_prompt, "gpt-4-turbo-preview")
        drug = re.search(MARKDOWN_PATTERN, response, re.DOTALL)
        if match:
            drug = match.group(1).strip()
        else:
            print("Error: Could not extract the checklist from the model's response.")
            drug = None

# There should be a drug
print('drug should be a drug')
print(f'drug {drug}')

# Getting the checklist from the drug by querying the dict
if drug:
    drug = drug.strip()
    if drug in drugs:
        checklist = drugs[drug]
    else:
        print("Error: Drug not found in the list of drugs.")
        checklist = None

# Now we can get updates to the checklist based on the transcript
if checklist:
    curr_prompt = prompt_checklist.format(
        drug=drug, checklist=checklist, transcript=chunk2)
    response = get_checklist(curr_prompt, "gpt-3.5-turbo")
    print(response)
    # Extract the updated checklist from the response
    match = re.search(JSON_PATTERN, response, re.DOTALL)
    if match:
        updated_checklist = match.group(1).strip()
    else:
        curr_prompt = prompt_checklist.format(
            drug=drug, checklist=checklist, transcript=chunk2)
        response = get_checklist(curr_prompt, "gpt-4-turbo-preview")
        match = re.search(JSON_PATTERN, response, re.DOTALL)
        if match:
            updated_checklist = match.group(1).strip()
        else:
            print(
                "Error: Could not extract the updated checklist from the model's response.")
            updated_checklist = None
    # Do a json.load on the updated checklist to update the system
    if updated_checklist:
        updated_checklist = json.loads(updated_checklist)
        print(updated_checklist)
    else:
        print("Error: Could not update the checklist.")

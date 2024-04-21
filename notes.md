npx create-next-app@latest gene-stepper --typescript --tailwind --eslint

- yes to src directory

npx shadcn-ui@latest init

add with normal shad way
https://ui.shadcn.com/docs/installation/next

https://codevoweb.com/integrate-fastapi-framework-with-nextjs-and-deploy/

activate conda base with version of python you like

```sh
conda activate 311

python -m venv venv

source venv/bin/activate

conda deactivate

pip install -r requirements.txt

npm install
```

Prompt

We are looking at a research proposal and a weakness of the proposal given by a reviewer. We'll be looking at the proposal a couple of paragraphs at a time and see if the paragraphs needs to be revised to address the weakness. If the paragraphs don't need to be changed, do not give an edit. Maintain the exact style and wording unless the change addresses the weakness.

Paragraph:

```md

```

Weakness

```md

```

Output the revised paragraph. Your revision based on the weakness should be in a md codeblock like you've seen above. Give an empty md codeblock if there should be no edit. Think step by step before giving your edit.

````

Have it reason Yes or No for if the paragraph is relevant
If Yes, do something about it.

We are looking at a research proposal and a weakness of the proposal given by a reviewer. We'll be looking at the proposal a paragraphs at a time and see if the paragraph needs to be revised to address the weakness.

Paragraph:

```md

````

Weakness

```md

```

Think step by step if the paragraph needs to be changed or not with respect to the given weakness. The last line of your response should be of the following format: 'ANSWER: $YESORNO' (without quotes) where YESORNO is one of Yes or No.

```

```

We need to think through what structure we want to make the data

- input:
  - weakness
    - input field
    - single weakness
  - essay
    - file input
    - split on frontend
    - send request for each paragraph
    - show original in input field and new in right

# What do we need to do?

what endpoints?
we need to save things

- i can let them save things?
- i just need to have websockets to haev the

i don't want to do real time diarization

- i want to process the audio in 1.5 min intervals and update the firebase
- i want to have the total convo processed by an LLM to check if a checklist is required
- if there is a current checklist then process the entire checklist against the transcript

10 sec endpoint

- get audio

  - make sure to prime the audio with good prompt
  - transcribe
  - send to gpt-3.5 for diarization
  - send to firebase

- endpoint for polling the transcripts

- have session
  - i did that for the gene pertubation one

If there is a name of any drug

- get a drug name in a certain format

To get the railway

- you need to have the NIX

Extract
on each update to the transcript

- need to check if doctor has prescribed anything

Aviation

- healthcare isn't there yet
  won't increase safety unless it is more convenient than the current approach
  25% people said they don't spend enough time and spends too much time on the ehr
  computer doesn't discriminate

- can weight all edge cases equally to promote equity

- check for conditions
  - what conditions?

Medication 44%
Diagnostic errors
Our health care workers are overworked. Nurses and doctors spend around a daily median 4.5 hours of their time on EHR notes. This type of draining work would affect the quality anyone's work. It's not just doctors that are affected. A frequent complaint on the part of patients is that they don't feel like their being listened to when their doctor is forced to stay in front of a screen.

As such we've seen an explosion of AI scribes which relieve this problem. But one avenue that hasn't been fully exploited is using this technology to prevent and aid doctors in maximizing patient safety.

- screen shots of like 5 different ones

Medication errors alone account 44% of patient safety problems. Diagnostic error is also the leading cause of preventable patient harm as well.

We also know that checklists save lives. (insert images of studies and checklist manifesto).

- This type of mentality is what makes the aviation industry so safe
- Ideally we'd be doing this in health care too, but things change much faster here than in aviation

Adding more work on the part of the doctor to keep up with the latest checklists would only worsen the problem we have of our medical {people} wanting to leave within two years (cite) even though it'd increase patient safety.

Luckily with state of the art AI agents and long form voice transcription we have a solution where we can bake our cake and eat it too!

- show the quality and patient safety venn diagram

With PreScribe we can alleviate the stress of our health care workers while also working on pressing issue of both medication errors and diagnostic errors.

As you saw in our demo, PreScribe is an assistant that watches over the doctor-patient interaction and checks off the latest medical checklists in real-time!

Having a ground truth of the latest medical checklists allow for an equitable increase in patient safety due to how they can bring up {}

We think in terms of the sheer frequency of use of such a tool combined with how overrepresented medication/diagnostic errors are combined with how eager medical worker are to reduce their time doing EHR notes, this is the most impactful idea we thought that can take advantage of the technology we have now.

- diagram multiplying all these

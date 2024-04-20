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

aviation
won't increase safety unless it is more convenient than the current approach
25% people said they don't spend enough time and spends too much time on the ehr
computer doesn't discriminate

- can weight all edge cases equally to promote equity

- check for conditions
  - what conditions?

medication 44%
diagnostic errors

Let's break this down:

-

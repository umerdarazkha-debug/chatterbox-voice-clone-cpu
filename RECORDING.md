# Recording a voice sample

The clone copies whatever it hears: your tone, pace, accent and the room you record in. A clean sample matters more than anything else.

## How to record

- 20-40 seconds of speech. Shorter than 10 seconds clones badly.
- A phone voice memo is fine. Hold it about a hand's width from your mouth.
- Quiet room: no fan, air conditioning or music. A room with curtains, a sofa or a full wardrobe sounds better than an empty one.
- Speak the way you want the clone to sound. Read it flat and the clone sounds flat.
- One take, no music, no edits. Leave a second of silence at the start and end.
- Any format works (`.wav`, `.m4a`, `.mp3`). If a file fails to load, convert it: `ffmpeg -i sample.m4a -ac 1 -ar 24000 my-voice.wav`

## Something to read

> Most people try a new tool once, get an average result, and give up on it.
>
> Here is what changed after a few weeks of using it every day.
>
> I gave it real files, real notes and one clear goal, and it stopped guessing.
>
> Last Tuesday it drafted the plan, wrote the first version, and checked my numbers before lunch.
>
> Sounds too easy? I thought so too.
>
> So try it on one small job tonight, and see what you get back.

## Check the result

Listen to the clone next to your real voice. If it sounds off:

| Sounds | Try |
|---|---|
| Rushed | `--cfg 0.3` |
| Flat or bored | raise `--exaggeration` to 0.6-0.7 |
| Over the top | lower `--exaggeration` to 0.3-0.4 |
| Echoey or noisy | record the sample again in a quieter, softer room |
| A word is wrong | change `--seed`, or spell the word the way it sounds |

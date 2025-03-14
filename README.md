# Personal Voice Assistant

Test taking on a personal locally hosted audio assistant for mac os x.
It is mainly based on the work of https://github.com/apeatling/ollama-voice-mac/
Mostly made for german input and output converting text back an forth.
Performance is ... slow

WARNING: needs python 3.12 not higher for pytorch at the moment

<video src="https://github.com/PatouChoubidou/assistant/blob/main/assets/vids/assistant.mp4" width="480" />



## tools in use
- python
- ollama
- model with function calling support -> llama3.1
- text-to-speech (tts): pyttsx3 
- speech-to-text (stt): whisper using torch
- language translation -> translator.py using ollama(llama3) for translation or translator2.py using Helsinki-NLP/opus-mt, but does not seem to improve performance
- interface: pygame

## apis in use
- untis - timetable school
- bvg - transportation berlin 
- tageschau - news
- wttr.in - wheather

## usage
- source myvenv/bin/activate: activate env
- maybe install requirements.txt -> pip install -r /path/to/requirements.txt
- python app.py

## functions: what can you ask for
- ask for the time
- ask for the date
- ask for the weekday
- ask for how many days until: input maybe 24.12.2024
- ask for timer on mac 
- tell a joke - killer feature
- ask for the current wheather in
- ask for todays timetable of your kids, in case "web untis" is in use
- ask for the next train or bus leaving next to my house - not yours: bvg api
- ask for the news: taken from german medium tagesschau.de 
#### mac os:
- open browser on <www.xyz.de>

### functions: work in progress:
- wikipedia search
- crawl a website - mostly blocked by data regulation consent button: using bs4

### functions: nice to have:
- tell me what is playin' in cinemas right now 
- ideas for what to cook and their receipts
- meta functions like: assistant close() via stt
- some sports api 

## What else might be missing 
- some rag function
- some memory for the last few interactions of conversation -> using ollama chat messages[]
- some loop for an ongoing conversation with functions like end this one, start new one,








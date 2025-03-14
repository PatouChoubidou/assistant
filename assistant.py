import sys
import pygame
import logging
import pyaudio
import pyttsx3
import whisper
from dotenv import dotenv_values
import os
import numpy as np
from ask_ollama_with_funcs import ask_ollama_func
import torch
import subprocess
import wave
import queue
import threading
import random
import time


config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
}

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

CANVAS_WIDTH = 512
CANVAS_HEIGHT = 200
CANVAS_BG_COLOR = (0,0,0)
FONT_SIZE = 25
CANVAS_BG_COLOR = (0,0,0)
CANVAS_MESSAGE_COLOR = (122, 210, 255)
CANVAS_MAX_MESSAGE_LEN_DISPLAY = 300

WAVE_LINE_WIDTH = 2
WAVE_LINE_COLOR = (122, 210, 255)
WAVE_LINE_COLOR_USER = (50, 205, 50)
WAVE_LINE_COLOR_GREEN = (50, 205, 50)

INPUT_FORMAT = pyaudio.paInt16
INPUT_CHANNELS = 1
INPUT_RATE = 16000
INPUT_CHUNK = 1024

class  Assistant:

    def __init__(self):
        logging.info("Initializing Assistant")
        
        programIcon = pygame.image.load('assets/imgs/icon.png')
        pygame.display.set_icon(programIcon)

        self.aiIsSpeaking = False
        self.hasTranslation = False

        self.clock = pygame.time.Clock()
        # pygame.display.set_icon(programIcon)
        self.bg_image = pygame.image.load("assets/imgs/bg-03_d.png")

        pygame.display.set_caption("Assistant")

        self.windowSurface = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), 0, 32)
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.audio = pyaudio.PyAudio()
        self.energy_list = [0] * 25
        '''
        sapi5 - SAPI5 on Windows
        nsss - NSSpeechSynthesizer on Mac OS X
        espeak - eSpeak on every other platform
        '''
        self.tts = pyttsx3.init("nsss")
        self.tts.setProperty('rate', self.tts.getProperty('rate') - 20)

        try:
            self.audio.open(format=INPUT_FORMAT,
                            channels=INPUT_CHANNELS,
                            rate=INPUT_RATE,
                            input=True,
                            frames_per_buffer=INPUT_CHUNK).close()
        except Exception as e:
            logging.error(f"Error opening audio stream: {str(e)}")
            self.wait_exit()

        self.display_message(config["ASSISTANT_MESSAGE_LOADING"])
        self.model = whisper.load_model(config['WHISPER_MODEL_PATH'])
        self.context = []
        self.display_message(config["ASSIST_MESSAGE_START_LISTENING"])


    async def sayHello(self):
        i_start = ["Guden, na was kann ich für dich tun?", 
                  "Hallo, Bonjour, konnichiwa",
                  "Was kann ich heute für Euch tun Eure Durchlaucht?",
                    "Boom,... was geht",
                    "Wusch, da bin ich wieder. Wie Gini aus der Wunderlampe...",
                    "Du hast drei Wünsche frei.",
                  ]
        sentence = i_start[random.randint(0, len(i_start)-1)] 
        await self.ai_speaking(sentence)


    def wait_exit(self):
        while True:
            self.display_message(config["ASSISTANT_MESSAGE_LOADING"])
            # self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    self.shutdown()


    async def shutdown(self):
        i_quit = ["Ich hau mich mal ne Runde auf's Ohr.", 
                  "OK..Dann......Dann werd ich wohl mal gehen.",
                  "Aha, also zurück in die Hundehütte.",
                    "Tschö mit ö",
                  ]
        sentence = i_quit[random.randint(0, len(i_quit)-1)] 
        await self.ai_speaking(sentence)
        """
        close all streams and quit pygame
        """
        logging.info("Shutting down Assistant")
        self.audio.terminate()
        pygame.display.quit()
        pygame.quit()
        sys.exit()


    def reset_waveform(self):
        """
        Visuals: flat the wavform line 
        """
        # self.windowSurface.fill(CANVAS_BG_COLOR)
        self.windowSurface.blit(self.bg_image, (0,0))
        pygame.draw.line(surface=self.windowSurface,
                         color=WAVE_LINE_COLOR,
                         start_pos=(0, CANVAS_HEIGHT/2),
                         end_pos=(CANVAS_WIDTH, CANVAS_HEIGHT/2),
                         width=WAVE_LINE_WIDTH
                        )
        pygame.display.update()

    '''
    # still working on that one
    def blit_text(self, text, pos, font, color=pygame.Color('black')):
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= CANVAS_MAX_MESSAGE_LEN_DISPLAY:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                self.windowSurface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
    '''

    def display_message(self, text):
        logging.info(f"Displaying message: {text}")
        
        LABEL_MARGIN = 20

        label = self.font.render(text
                                 if (len(text)<CANVAS_MAX_MESSAGE_LEN_DISPLAY)
                                 else (text[0:CANVAS_MAX_MESSAGE_LEN_DISPLAY]+"..."),
                                 1,
                                 CANVAS_MESSAGE_COLOR)

        size = label.get_rect()[2:4]
        self.windowSurface.blit(self.bg_image, (0,0))
        self.windowSurface.blit(label, (CANVAS_WIDTH/2 - size[0]/2, CANVAS_HEIGHT/2 - size[1]/2))
        # self.blit_text(text, (CANVAS_WIDTH/2, CANVAS_HEIGHT/2), self.font, CANVAS_MESSAGE_COLOR)

        pygame.display.flip()


    async def waveform_from_mic(self, key = pygame.K_SPACE) -> np.ndarray:
        """
        Get audio input from user and display the waveform
        Returns:
            An numpy array of the audio data
        """
        logging.info("Capturing waveform from microphone")
       
        stream = self.audio.open(format=INPUT_FORMAT,
                                 channels=INPUT_CHANNELS,
                                 rate=INPUT_RATE,
                                 input=True,
                                 frames_per_buffer=INPUT_CHUNK)
        frames = []

        LAST_X = 0
        LAST_Y = 0 + CANVAS_HEIGHT/2

        while True:
            pygame.event.pump() # process event queue
            pressed = pygame.key.get_pressed()
            if pressed[key]:
                # self.windowSurface.fill(CANVAS_BG_COLOR)
                self.windowSurface.blit(self.bg_image, (0,0))
                data = stream.read(INPUT_CHUNK)
                d = np.frombuffer(data, dtype=np.int16)
                # Normalization to get Data between -1 and 1 -> int 16 => 32767
                norm = [x / 32767 for x in d]
                # one could use this as well or a max()
                # blockLinearRms=np.sqrt(np.mean(np.pow(data_strich, 2)))       
                
                # visualize the waveform
                X_SHIFT = CANVAS_WIDTH / INPUT_CHUNK   
                ZOOM_FACTOR = CANVAS_HEIGHT
                
                for i, val in enumerate(norm):
                    val = val * ZOOM_FACTOR
                    if i > 0:
                        pygame.draw.line(
                            surface=self.windowSurface,
                            color=WAVE_LINE_COLOR_USER,
                            start_pos=(LAST_X, LAST_Y),
                            end_pos=(i*X_SHIFT, val + (CANVAS_HEIGHT/2)),
                            width=WAVE_LINE_WIDTH,
                        )

                    LAST_X = i*X_SHIFT
                    LAST_Y = val + CANVAS_HEIGHT/2
              
                pygame.display.update()   
                frames.append(data)   
                
            else:
                break
        # flat the waveform line again
        self.reset_waveform()
        stream.stop_stream()
        stream.close() 

        return np.frombuffer(b''.join(frames), np.int16).astype(np.float32) * (1 / 32768.0)
    

    async def speech_to_text(self, waveform):
        """
        Transcribe the spoken into text using whisper as model
        Params:
            waveform: input from mic
        Returns: 
            text: str - the transcribed audio
        """
        logging.info("Converting speech to text")
        
        # FIFO queue
        result_queue = queue.Queue()

        def transcribe_speech():
            try:
                logging.info("Starting transcription")
                transcript = self.model.transcribe(waveform,
                                                language=config["WHISPER_LANG"],
                                                fp16=torch.cuda.is_available())
                logging.info("Transcription completed")
                text = transcript["text"]
                print('\nMe:\n', text.strip())
                result_queue.put(text)
            except Exception as e:
                logging.error(f"An error occurred during transcription: {str(e)}")
                result_queue.put("")

        transcription_thread = threading.Thread(target=transcribe_speech)
        transcription_thread.start()
        transcription_thread.join()

        return result_queue.get()


    async def ask_ollama(self, prompt):
        """
        Ask a model to answer the question using build in functions
        """
        logging.info(f"Asking ollama with prompt: \n{prompt}")
        res = await ask_ollama_func(prompt)
        return res
    

    async def generateAiffFromText(self, txt):
        """
        Convert text to speech using pytssx3
        Params:
            txt
        Returns:
            saves an audio file as aiff
        """
        # choose engine by system espeak, nsss, avspeech 
        engine = self.tts
        # rate = engine.getProperty('rate')
        # engine.setProperty('rate', rate) # default 200
        # engine.setProperty("pitch", 75)  # Set the pitch (default 50) to 75 out of 100 - doesnt work with nsss
        engine.setProperty('voice', config["TTS_VOICE"])
        engine.say(" ") # this is a workaround for pyttsx3 not beeing able to save files 
        engine.save_to_file(txt, 'output.aiff') # says it can save as wav but actually is aiff Format
        engine.runAndWait()


    async def convertAiffToWave(self):
        """
        Convert an aiff file to wave
        """
        cmd2 = f"ffmpeg -y -i output.aiff -ac 2 output.wav" 
        subprocess.call(cmd2, shell=True)


    async def openWaveAndDisplayWaveform(self):
        """
        Play a wave audio file and visualize the waveform
        """
        file_name = 'output.wav'
        with wave.open(file_name, 'rb') as wf:
            '''
            wave_params(nchannels=1, sampwidth=2, framerate=22050, nframes= depends, comptype='NONE', compname='not compressed')
            '''
            
            stream = self.audio.open(format=self.audio.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            
            OFFSET_TOP = CANVAS_HEIGHT/2
            LAST_X = 0
            LAST_Y = 0 + OFFSET_TOP 
            
            while len(data := wf.readframes(INPUT_CHUNK)):
                self.windowSurface.blit( self.bg_image, ( 0,0 ) )

                stream.write(data)
                d = np.frombuffer(data, np.int16)
                norm = [ x / 32767 for x in d]
                
                X_SHIFT = CANVAS_WIDTH / INPUT_CHUNK   
                ZOOM_FACTOR = CANVAS_HEIGHT
                    
                for i, val in enumerate(norm):
                    # logging.info(val)
                    val = val * ZOOM_FACTOR
                    if i > 0:
                        pygame.draw.line(
                                surface=self.windowSurface,
                                color=WAVE_LINE_COLOR,
                                start_pos=(LAST_X, LAST_Y),
                                end_pos=(i*X_SHIFT, val + OFFSET_TOP),
                                width=WAVE_LINE_WIDTH
                        )
                    LAST_X = (i*X_SHIFT)
                    LAST_Y = val + OFFSET_TOP
                
                pygame.display.update()      

            logging.info(f"end of speaking")
            logging.info(f"\n file: output.wav,\n Params: {wf.getparams()}, data length: {len(data)}")
            
            time.sleep(0.2)
            
            self.reset_waveform()
            stream.stop_stream()
            stream.close()
            

    async def ai_speaking(self, txt):
        """
        All steps from taking text, saving it as audio and playing it.
        """
        await self.generateAiffFromText(txt)
        logging.info(f"aiff generated from text")
        # here we need to convert it to real wav
        await self.convertAiffToWave()
        logging.info(f"converted aiff to wave")
        # here I got some problems in visualization 
        await self.openWaveAndDisplayWaveform()
        logging.info(f"opened wave and displayed waveform")
        
        
                       



   
        
        
        

    
    

    



        
        
        
         


        
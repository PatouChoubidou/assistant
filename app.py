import sys
import pygame
from assistant import Assistant
import logging
import time
import asyncio
import locale
from multiprocessing import Pool
import translator2


async def main():
    logging.info("Starting Assistant")
    pygame.init()

    ass = Assistant()
    ass.hasTranslation = True

    push_to_talk_key = pygame.K_SPACE
    quit_key = pygame.K_ESCAPE

    currentLoc = locale.getlocale()
    logging.info(f"Your system Language is: {currentLoc[0]}")

    await ass.sayHello()
    #INSIDE OF THE GAME LOOP
    
    ass.display_message('push space to talk')
    while True:
        
        ass.clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                await ass.shutdown()
            
            if event.type == pygame.KEYDOWN:
                if event.key == push_to_talk_key:
                    
                    speech = await ass.waveform_from_mic(push_to_talk_key)

                    ass.display_message('processing...')

                    transcription = await ass.speech_to_text(waveform=speech)
                    logging.info(f"\nTransciption: {transcription}\n")

                    if ass.hasTranslation:
                        # inputInEnglish = await translator.translateFromLocaleToEnglish(transcription)
                        transcription = await translator2.translate_de_en(transcription)
                        logging.info(f"\nin english: {transcription}\n")

                    answer = await ass.ask_ollama(transcription)
                    logging.info(f"\n Antwort Model: {answer}\n")
 
                    ass.display_message(answer)

                    if ass.hasTranslation:
                        # answerInUserLang = await translator.translateFromEnglishToLocale(answer)
                        answer = await translator2.translate_en_de(answer)
                        logging.info(f"\n in deutsch: {answer}\n")

                    await ass.ai_speaking(answer)

                    ass.display_message('push space to talk')
 

                if event.key == quit_key:
                    logging.info("Quit key pressed")
                    await ass.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
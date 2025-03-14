import ollama
from ollama import AsyncClient, ChatResponse
import locale
import logging

'''
This translator is using some ollama model for translation
eg. llama3
'''

async def translateFromLocaleToEnglish(txt: str):
    """
    Takes a text in local language and output it in english
    """
    logging.info("translating input to english")
    system_lang = 'english'
    currentLoc = locale.getlocale()
    if currentLoc[0] == 'de_DE':
         system_lang = 'german'
   
    prompt = f"""
        You are a language translation model.
        Translate the following Text in german to english:
        {txt}
        Output the only the translated text without any explanation nor comment.
    """
    client = ollama.AsyncClient()   
    result = await client.chat(
        'llama3',
        messages=[{'role': 'user', 'content': prompt }],
    )
    
    return result.message.content


async def translateFromEnglishToLocale(txt: str):
    logging.info("translating text to system language")
    system_lang = 'english'
    currentLoc = locale.getlocale()
    if currentLoc[0] == 'de_DE':
         system_lang = 'german'
   
    prompt = f"""
        Translate the following Text in english to {system_lang}.
        Text to translate: {txt}

        Output the only the translated text without any explanation or comment.
    """

    client = ollama.AsyncClient()   
    result = await client.chat(
        'llama3',
        messages=[{'role': 'user', 'content': prompt }],
    )
    
    return result.message.content
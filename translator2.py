import asyncio
# sentencepiece splits text into chunks and weights
from transformers import pipeline
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

'''
This translator is using Helsinki-NLP/opus-mt for translation
'''

async def load_model_from_hf():
    '''
    Download the model from huggingface and save it
    '''
    # Load the model and tokenizer from Hugging Face
    # model_name= "Helsinki-NLP/opus-mt-de-en"
    model_name = "Helsinki-NLP/opus-mt-en-de"  # You can replace this with any model name
    model = AutoModelForSeq2SeqLM.from_pretrained(f"{model_name}")
    # model = AutoModelForSequenceClassification.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(f"{model_name}")

    model.save_pretrained(f"{model_name}")
    tokenizer.save_pretrained(f"{model_name}")


async def translate_en_de_withPipeline(txt: str) -> str:
    '''
    translation unsing transformers pipeline
    '''
    model_name = "Helsinki-NLP/opus-mt-en-de" 
    model = AutoModelForSeq2SeqLM.from_pretrained(f"{model_name}")
    tokenizer = AutoTokenizer.from_pretrained(f"{model_name}")
    task_name = f"translation_en_to_de"
    translator = pipeline(task=task_name, model=model, tokenizer=tokenizer)
    translated = translator("You are a genius")[0]["translation_text"]
    print(translated)


async def translate_en_de(txt: str):
    """
    Takes a in english text and translates it in german
    Params:
        txt: str -> the english to be translated
    Returns:
        txt: str -> the german version of txt
    """

    model_name1 = "Helsinki-NLP/opus-mt-en-de"
   
    local_model = AutoModelForSeq2SeqLM.from_pretrained(f"{model_name1}")
    local_tokenizer = AutoTokenizer.from_pretrained(f"{model_name1}")
   
    # tokenize imput, pt for pyttorch tensor ?
    inputs = local_tokenizer.encode(txt, return_tensors="pt", max_length=512, truncation=True)
    outputs = local_model.generate(inputs)
    result = local_tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(result)
    return result


async def translate_de_en(txt: str):
    """
    Takes a in german text and translates it in english
    Params:
        txt: str -> the german to be translated
    Returns:
        txt: str -> the english version of txt
    """

    model_name2 = "Helsinki-NLP/opus-mt-de-en"
    local_model = AutoModelForSeq2SeqLM.from_pretrained(f"{model_name2}")
    local_tokenizer = AutoTokenizer.from_pretrained(f"{model_name2}")

    # tokenize input, pt for pyttorch tensor ?
    inputs = local_tokenizer.encode(txt, return_tensors="pt", max_length=512, truncation=True)
    # feed it to the model
    
    # using greedy search
    # greedy_outputs = local_model.generate(inputs)
    # decode the result tokens
    # result = local_tokenizer.decode(greedy_outputs[0], skip_special_tokens=True)

    # or using beam algorithm
    beam_outputs = local_model.generate(inputs, num_beams=3)
    result = local_tokenizer.decode(beam_outputs[0], skip_special_tokens=True)
    print(result)
    return result
 

async def main():
    # load_model_from_hf()
    # translate_en_de("I am a genius")
    translate_de_en("Ich bin ein Holzfäller")
    # translate_en_de_withPipeline("I am a genius")


if __name__ == '__main__':
    asyncio.run(main())
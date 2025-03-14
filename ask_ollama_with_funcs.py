import ollama
from ollama import ChatResponse
import my_funcs
import logging

async def ask_ollama_func(prompt):
    logging.info("Inside ask ollama func")
    
    client = ollama.AsyncClient()
   
    # this time we have two functions
    avaiable_funcs = {
        'what_day_is_it': my_funcs.what_day_is_it,
        'get_the_weather_in': my_funcs.get_the_weather_in,
        'what_weekday_is_it': my_funcs.what_weekday_is_it,
        'what_time_is_it': my_funcs.what_time_is_it,
        'how_many_days_until': my_funcs.how_many_days_until,
        'wikisearch_for_topic': my_funcs.wikisearch_for_topic,
        'get_text_spreadsheet': my_funcs.get_text_spreadsheet,
        'crawl_website': my_funcs.crawl_website,
        'get_todays_schedule_of': my_funcs.get_todays_schedule_of,
        'tell_a_joke': my_funcs.tell_a_joke,
        'get_news_of_the_day': my_funcs.get_news_of_the_day,
        'start_a_timer': my_funcs.start_a_timer,
        'when_is_the_next_bus_going_to_S_bahn': my_funcs.when_is_the_next_bus_going_to_S_bahn,
        'when_u5_from_biesdorf_to_mitte': my_funcs.when_u5_from_biesdorf_to_mitte,
        'when_is_the_next_bus_going_to_U_Tierpark': my_funcs.when_is_the_next_bus_going_to_U_Tierpark,
        'no_function_fits_the_question': my_funcs.no_function_fits_the_question,
        'openBrowser': my_funcs.openBrowser
    }


    response: ChatResponse = await client.chat(
            'llama3.2',
            messages=[{'role': 'user', 'content': prompt }],
            tools=[my_funcs.get_the_weather_in, 
                   my_funcs.what_day_is_it, 
                   my_funcs.what_weekday_is_it,
                   my_funcs.what_time_is_it,
                   my_funcs.how_many_days_until,
                   my_funcs.wikisearch_for_topic,
                   my_funcs.get_text_spreadsheet, 
                   my_funcs.crawl_website,
                   my_funcs.get_todays_schedule_of,
                   my_funcs.tell_a_joke,
                   my_funcs.get_news_of_the_day,
                   my_funcs.start_a_timer,
                   my_funcs.when_is_the_next_bus_going_to_S_bahn,
                   my_funcs.when_is_the_next_bus_going_to_U_Tierpark,
                   my_funcs.when_u5_from_biesdorf_to_mitte, 
                   my_funcs.no_function_fits_the_question,
                   my_funcs.openBrowser
                ],
        )

    print('the response: ', response, '\n\n')

    #check if tool call is initated
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if function_to_call := avaiable_funcs.get(tool.function.name):
                print('\nCalling function: ', tool.function.name)
                print('\nArguments: , \n', tool.function.arguments, "\n")
                print('\nFunction Output: \n', function_to_call(**tool.function.arguments), "\n")
                response = function_to_call(**tool.function.arguments)
            else: 
                print('\nFunction: ', tool.function.name, 'not found') 

      
    prompt2 = f"""
            Answer the question below:
            Use the result of this web search {response}.

            If asked for a schedule answer in the format:
            Timeslot, lesson name, given by teacher
            e.g. 1. Stunde Mathematik bei Frau Chevalier

            In case you are asked for the current time answer in the format:
            e.g It is Hours Minutes

            If asked for the weekday answer:
            eg. It is a wonderfull <weekday>

            If asked to open the browser just replied you did so.

            if asked for starting a timer 
            do not simulate a timer by counting down instead just respond you started one.

            If asked for the news of the day just output all articles as given:
            e.g. news 1, title , slug, topline

            If asked for the content of webpage try to make sense of the html and give a short comprehension of the websites content and purpose.

            Do not make anything up. 
            Don't mention any of the upper choices if you do not have the information.

            Question: {prompt}  

            Answer:           
     """
        
    result = await client.chat(
        'llama3',
        messages=[{'role': 'user', 'content': prompt2 }],
    )

    print('\nexplanation: ', result.message.content)

    return result.message.content
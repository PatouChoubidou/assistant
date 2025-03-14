import bs4
import requests
from datetime import datetime, date
from dotenv import dotenv_values
import pandas as pd
import untis
import json
import subprocess
import time
from datetime import datetime, timedelta
import bvg


def no_function_fits_the_question():
    """
    This is a fallback in case no function fits the users question
    Returns:
        A string with further information on how to handle missing requests
    """
    return f"It seems like no function or web search fits the user intention. Just answers the question as good as you can based on your training data."


def openBrowser(url = 'wwww.google.com'):
    """
    Opens a browser on mac with the given url
    Params:
        url: str - the url to visit
    Returns:
        message: str - confirmation of trying
    """
    # maybe one could use webbrowser: https://docs.python.org/3/library/webbrowser.html

    browsers = ['Google Chrome.app', 'Safari.app', 'Firefox.app']

    if url.startswith('http'):
        cmd =f"open -a '{browsers[0]}' '{url}'"
    else:
        cmd =f"open -a '{browsers[0]}' 'https://{url}'"
   
    print(f"browser cmd: {cmd}")
    try:
        subprocess.run(args=[cmd], shell=True)
    except:
        cmd =f"open -a {browsers[0]}'"
    
    return f"I tried opening the browser with {url}"


def wikisearch_for_topic(searchword):

    """
    Search wikipedia for a word / topic
    """

    try:
        URL = "https://en.wikipedia.org/w/api.php"

        PARAMS = {
            "action": "parse",
            "page": searchword,
            "format": "json"
        }

        my_headers = {
        'User-Agent': 'patricekoebel@gmail.com'
        }

        response = requests.get(url=URL, params=PARAMS, headers=my_headers)
        data = response.json()
        print(data)
        return data["parse"]["text"]["*"]
    except:
        return "no information found"

    
def crawl_website(url):
    """
    Get the Text from a web page
    Get Information on a web page
    """

    my_headers = {
        'User-Agent': 'bonzo@gmail.com'
        }
    try:
        response = requests.get(url, headers=my_headers)
        print(response.status_code)
        print(response.text)
    
        if response:
            html = bs4.BeautifulSoup(response.text, 'html.parser')

            title = html.select("#firstHeading")[0].text
            out = title+"\n"
            
            paragraphs = html.select("p")
            for para in paragraphs:
                out += "\n"+para.get_text(' ')

            print('\n\n out: ',out)

            return out
    except:
        return "did not work"


def what_time_is_it():
    """
    Get the current time.
    Returns: the time in format Hour Minutes Seconds
    """
    return datetime.today().strftime('%H:%M:%S')


def start_a_timer(hours, minutes, seconds):
    """
    Function to create and start timer on mac os x
    Params: 
        hours: hours as str
        minutes: minutes as str
        seconds: seconds as str
    """
    h = 0
    m = 0 
    s = 0
    if hours == "" or hours == 0:
        h = 0
    else:
        h = int(hours)

    if minutes == "" or minutes == 0:
        m = 0
    else:
        m = int(minutes)

    if seconds == "" or seconds == 0:
        s = 0
    else:
        s = int(seconds)
    # all to secs
    sleep_time = int(h) * 3600 + int(m) * 60 + int(s)
    # only works on mac
    cmd =f"sleep {sleep_time}s; say Time is up;"
    # Popen to run it in seperate deamon process ...
    subprocess.Popen(args=[cmd], shell=True, name="patrices_timer")
    
    return f"timer mit {h} hours {m} minutes and {s}seconds has started"


def what_day_is_it():
    """
    Get the current date
    """
    now = datetime.now()
    formatted = f"{now.strftime('%A')} the {now.strftime('%d')} of { now.strftime('%B')} {now.strftime('%Y')}"
    return formatted


def what_weekday_is_it():
    """
    Get the todays weekday
    """
    weekdays=['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekdayNr = datetime.now().isoweekday()
    return weekdays[weekdayNr]


def how_many_days_until(datum):
    """
    Count the days to a upcoming date from today on
    """
    try:
        today = date.today()
        future = datetime.strptime(datum, '%Y-%m-%d').date()
        if today > future:   
            return f"Only {(today-future).days} day to go."
        else:
            return f"Only {(future-today).days} day to go."
    except:
        return "This could not be converted"


def when_is_the_next_bus_going_to_S_bahn(minutes=10):
    """
    Get the next bus from Kötztinger Strasse which is leaving for station S Karlshorst 
    Params:
        minutes = int: start_time of the request
    Returns:
        A string with the time of the bus departure
    """
    return bvg.when_is_the_next_bus_going_to_S_bahn(minutes)


def when_is_the_next_bus_going_to_U_Tierpark(minutes=10) -> str:
    """
    Get the next bus going to metro station U Tierpark 
    Params:
        minutes = int: start_time of the request
    Returns:
        A string with the time of the bus departure
    """
    return bvg.when_is_the_next_bus_going_to_U_Tierpark(in_minutes=minutes)


def when_u5_from_biesdorf_to_mitte(minutes=10):
    """
    Get the time the berlin metro line U5 is leaving from station Biesdorf-Süd to Berlin Mitte
    Params:
        minutes: int: the start_time to look for departures
    Returns:
        A String discribing the depature time 
    """
    return bvg.when_u5_from_biesdorf_to_mitte(minutes)

    
def get_the_weather_in(city):
    """
    Get information on how the weather will be in a city
    from: https://github.com/chubin/wttr.in
    """
    try:
        url = f'https://wttr.in/{city}?format="City: %l:+,Condition: %C+,Temperature: %t+felt temperatur: %f+,Wind: %w+,Rain: %p+%S"'
        response = requests.get(url)
        return f"Today is {datetime.now()}\n {response.text}"
    except:
        return 'Look out the window you jerk'
   

def get_todays_schedule_of(name:str):
    """
    Get information about the timetable of Margaux or Tosca for today.
    Information on the lessons and the teachers involved.
    Params:
        name: str
    Returns: 
        list classes of today
    """
    return untis.getTimeTableOfTheDayFor(name)


def tell_a_joke():
    """
    Tell me a joke from https://witzapi.de/
    Do you know a joke about?
    Parameter:
        None
    Returns:
        A new Joke in format: joke setup - joke delivery
    """
    try:
        # url = f'https://witzapi.de/api/joke/?language=de'
        url = f'https://witzapi.de/api/joke/'
        response = requests.get(url)
        j = response.json()
        
        outstr = f"\n"
        outstr += f"{j[0]['text']}\n"
        outstr += f"\n"
        # print(json.dumps(j, indent=4, sort_keys=True))
        return f"Joke is:\n {outstr}"
    except:
        return 'I cant think of any joke'


'''
def tell_a_joke():
    """
    Tell me a joke.
    Do you know a joke about?
    Returns:
        A new Joke to tell in two formats: single joke or in format:
        Joke setup
        Joke delivery

    But the whole api does not seem to be very funny
    """
    try:
       
        url = f'https://v2.jokeapi.dev/joke/Any?lang=de&blacklistFlags==racist,sexist'
        response = requests.get(url)
        j = response.json()
        outstr = f''
        if(j['type'] == 'twopart'):
            outstr += f"\n"
            outstr += f"{j['setup']}\n"
            outstr += f"{j['delivery']}\n"
            outstr += f"\n"
        else:
             outstr += f"{j['joke']}"
        print(json.dumps(j, indent=4, sort_keys=True))
        return f"Joke is\n {outstr}"
    except:
        return 'I cant think of any joke'
'''


def get_text_spreadsheet():
    '''
    creating a dataframe from a test spreadsheet 
    '''
    
    dataframe = pd.read_excel('assets/excel/test.xlsx', na_values = "nicht da", sheet_name="Peter")

    return dataframe


def get_news_of_the_day(ressort = 'ausland'):
    '''
    Get the headlines and news from german news plattform tagesschau.de via api
    Params:
        ressort: "ausland" is the default value
        possible values: "inland", "ausland", "wirtschaft", "sport", "video", "investigativ", "wissen"

    Returns: 
        A string containing 10 news. 
        Each in format: arcticle number, title, slug, first sentence.

    '''
    server = 'https://www.tagesschau.de'
    endpoint_homepage = "/api2u/hompage/"
    endpoint_get_news = "/api2u/news/"
    # endpoint_get_news_resort = ["inland", "ausland", "wirtschaft", "sport", "video", "investigativ", "wissen"]
    try:    
        url = f'{server}{endpoint_get_news}?ressort={ressort}'
        response = requests.get(url)
        response_dict = response.json()

        outstr = "" 
        news_list = response_dict['news']
        max_n = 10
        for i, news in enumerate(news_list[0:max_n]):  
            outstr += f"\n"
            outstr += f"[[slnc 400]]"
            outstr += f"Artikel {i+1}:\n"
            outstr += f"title: {news['title']}\n"
            outstr += f"topline: {news['topline']}\n"
            outstr += f"first sentence: {news['firstSentence']}"
            outstr += f"\n"

        print(f"news: \n {news['title']} \n")
       
        return f"All news im ressort{ressort}:\n {outstr}"
    except:
        return 'I am unable to contact the new feed.'



    
   
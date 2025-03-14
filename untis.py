import json
import os
import webuntis
import datetime
from dotenv import dotenv_values
from difflib import SequenceMatcher


config = {
    **dotenv_values(".env"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def getTimeTableOfTheDayFor(name: str):

    '''
    https://www.python-forum.de/viewtopic.php?t=57973
    read the docs of webuntis python very good 
    not much is possible as normal student
    '''

    print(f"config: {config}")
    

    # use fuzzywuzzy?
    if similar(name, config["NAME_OF_KID_ONE"]) >= 0.4:
        LOG_IN = json.loads(config["WEBUNTIS_T"].replace("\n", " "))
    if similar(name, config["NAME_OF_KID_TWO"]) >= 0.4:
        LOG_IN = json.loads(config["WEBUNTIS_M"].replace("\n", " ")) 

    s = webuntis.Session(
        server=LOG_IN["server"],
        username=LOG_IN["username"],
        password=LOG_IN["password"],
        school=LOG_IN["school"],
        useragent=LOG_IN["useragent"]
    )

    s.login()

    today = datetime.date.today().strftime("%Y%m%d")
    monday=today
    friday=today

    table = s.my_timetable(start=monday, end=friday).to_table()

    # print('\n Type of table : \n', type(table))

    '''
    for the table one should know that it goes through the rows of the time span chosen
    row by row and not by column per day as in a calender.
    so it might be easier to go day by day each a new request...
    '''

    '''
        period object looks like this:
        {
            'id': num,
            'date': num,
            'startTime': num,
            'endTime': num,
            'kl': [{'id': num}], -> class
            'te': [{id: num}],-> teacher
            'su': [{'id: num'}], -> subject
            'ro': [{'id': num}],
            'lsnumber': num, -> lessonNumber or...
            'info': str, -> additional infos
            'activityType': str, -> saying unterricht or 
        }
    '''
    # sadly hard coded without further api access
    my_teacherMap = json.loads(config["TEACHER_MAP"].replace("\n", " "))
    

    outstring = f"{name}'s Stundenplan sieht heute so aus: {datetime.date.today().strftime("%d %m %Y")} \n\n"

    for i, row in enumerate(table):
        
        item = list(row[1][0][1])[0]
        # print(item.id)
        outstring += f'Stunde: {i+1} \n'
        
        outstring += f'Start: {item.start} \n'
        
        outstring += f'Ende: {item.end} \n'
        
        outstring += f'Fach: {item.subjects[0].long_name} \n'
    
        outstring += f'Klasse: {item.klassen[0].long_name} \n'
        if item.rooms: 
            outstring += f'Raum: {item.rooms[0]} \n'

        if "info" in item._data:
            outstring += f'Raum: {item._data} \n' 

        teacher_id = item._data['te'][0]['id']
        if str(teacher_id) in my_teacherMap:
            outstring += f'Lehrer: {my_teacherMap[str(teacher_id)]}\n' 
        else:
            outstring += f'Lehrer id: {teacher_id}\n'

        outstring += f'Aktivität : {item.activityType} \n\n'


    print(outstring)
    s.logout()

    return outstring
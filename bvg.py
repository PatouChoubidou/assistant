from datetime import datetime, timedelta
import requests
from zoneinfo import ZoneInfo

"""
    https://v6.bvg.transport.rest/api.html
"""

def get_station_id_by_name(station_name) -> str:
    """
    Get the bvg location id by station name e.g. S+U Alexanderplaz
    
    Params:
        station_name: str
    Returns:
        id: str
    """
    try:
        url = f'https://v6.bvg.transport.rest/locations?query={station_name}'
        response = requests.get(url)
        print(f"response_code: {response.status_code}")
        json = response.json()
        first_item = json[0]
        id = first_item['id']

        print(f"station id: {id}\n station name: {first_item['name']}")
       
        return id
    except:
        return "Can't contact server"


def when_is_the_next_bus_going_to_U_Tierpark(in_minutes=10) -> str:

    """
    Get the next bus leaving from Kötztinger Strasse to U Tierpark.
    """

    my_headers = {
        'User-Agent': 'Api test'
    }

    nowInIso = ( datetime.now(ZoneInfo('Europe/Berlin')) + timedelta(minutes=int(in_minutes))).isoformat()
    print(f"now in iso: {nowInIso}")
    nowInIso = nowInIso.split('+')[0]

    outstr = f''
    koetztinger_station_id=900162518
    tierpark_station_id=900161002

    try:
        url = f'https://v6.bvg.transport.rest/stops/{koetztinger_station_id}/departures?&duration=20&direction={tierpark_station_id}&reuslts=1&when={nowInIso}'
        response = requests.get(url, headers=my_headers)
        print(response.status_code)
        json = response.json()
        
        departure_list = json['departures']
        first_departure = departure_list[0]
        # print(first_departure)
        
        departure_time = first_departure['when']
        print(f"depature time: {departure_time}")
       
        if departure_time is None:
            remarks_list = first_departure['remarks']
            print(remarks_list)
            for remark in remarks_list:
                print(remark)
                if 'text' in remark:
                    outstr += f"{remark['text']}\n"
                    
            print(outstr)
        else:
            # "2025-01-27T15:52:00+01:00"
            dst = departure_time.split('+')[1] # 01:00
            dst_hours = dst.split(':')[0] # e.g 01
            dst_min = dst.split(':')[1] # e.g 00
            d = datetime.fromisoformat(departure_time)
            hour_str = str(d.hour - int(dst_hours)).zfill(2)
            min_str = str(d.minute - int(dst_min)).zfill(2)
            outstr += f"The next bus of line 296 is coming {hour_str}:{min_str}"
        return f"Result: {outstr}"
    except:
        return "Can't figure out when the next bus is leaving"


def when_is_the_next_bus_going_to_S_bahn(in_minutes=10) -> str:

    """
    Get the next bus leaving from Kötztinger Strasse to S Karlshorst
    """

    my_headers = {
        'User-Agent': 'Api test'
    }

    nowInIso = ( datetime.now(ZoneInfo('Europe/Berlin')) + timedelta(minutes=int(in_minutes))).isoformat()
    print(f"now in iso: {nowInIso}")
    nowInIso = nowInIso.split('+')[0]

    outstr = f''
    koetztinger_station_id=900162518
    s_karlshorst_station_id=900162001

    try:
        url = f'https://v6.bvg.transport.rest/stops/{koetztinger_station_id}/departures?&duration=20&direction={s_karlshorst_station_id}&reuslts=1&when={nowInIso}'
        response = requests.get(url, headers=my_headers)
        print(response.status_code)
        json = response.json()
        
        departure_list = json['departures']
        first_departure = departure_list[0]
        # print(first_departure)
        
        departure_time = first_departure['when']
        print(f"depature time: {departure_time}")
       
        if departure_time is None:
            remarks_list = first_departure['remarks']
            print(remarks_list)
            for remark in remarks_list:
                print(remark)
                if 'text' in remark:
                    outstr += f"{remark['text']}\n"
                    
            print(outstr)
        else:
            # "2025-01-27T15:52:00+01:00"
            dst = departure_time.split('+')[1] # 01:00
            dst_hours = dst.split(':')[0] # e.g 01
            dst_min = dst.split(':')[1] # e.g 00
            d = datetime.fromisoformat(departure_time)
            hour_str = str(d.hour - int(dst_hours)).zfill(2)
            min_str = str(d.minute - int(dst_min)).zfill(2)
            outstr += f"The next bus of line 296 is coming {hour_str}:{min_str}."
        return f"Result: {outstr}"
    except:
        return "Can't figure out when the next bus is leaving"
    


def when_u5_from_biesdorf_to_mitte(in_minutes=10):

    """
    returns when the next metro line u5 leaving from biesdorf-süd to berlin mitte
    """
   
    nowInIso = ( datetime.now(ZoneInfo('Europe/Berlin')) + timedelta(minutes=int(in_minutes)) ).isoformat()
    print(f"now in iso: {nowInIso}")
    # request doesnt like the ZoneInfo...
    nowInIso = nowInIso.split('+')[0]

    outstr = f''

    biesdorf_station_id=900171005
    alex_station_id=900100003
    su_hauptbahnhof_id=900003201

    try:
        url = f'https://v6.bvg.transport.rest/stops/{biesdorf_station_id}/departures?&duration=10&direction={su_hauptbahnhof_id}&reuslts=1&when={nowInIso}'
        response = requests.get(url)
        print(f"response code: {response.status_code}")
        json = response.json()
        departure_list = json['departures']
        first_departure = departure_list[0]
        departure_time = first_departure['when']
        print(f"departure_time: {departure_time}")
       
        if departure_time is None:
            remarks_list = first_departure['remarks']
            print(remarks_list)
            for remark in remarks_list:
                print(remark)
                if 'text' in remark:
                    outstr += f"{remark['text']}\n"
        else:
            # reply is "2025-01-28T11:15:00+01:00" isoformat
            # extract the time difference and add it in the end
            # for Berlin it should be +1 hr in winter and +2 in summer to utc
            dst = departure_time.split('+')[1]
            dst_hours = dst.split(':')[0]
            dst_min = dst.split(':')[1]
            d = datetime.fromisoformat(departure_time)
            hour_str = str(d.hour - int(dst_hours)).zfill(2)
            min_str = str(d.minute - int(dst_min)).zfill(2)
            outstr += f"The next ubahn from biesdorf in direction mitte is coming {hour_str}:{min_str}."
        return f"Result: {outstr}"
    except:
        return "Can't figure out when the next ubahn is leaving"
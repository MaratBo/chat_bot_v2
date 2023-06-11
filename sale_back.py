import datetime
import json
from dotenv import load_dotenv
import os
import requests
import time
import bucket


load_dotenv()
token = os.getenv('MANAGER_TOKEN')
URL = 'https://apiauto.ru/1.0/comeback'
date_today = datetime.datetime.now()
t1 = datetime.datetime.today().strftime('%Y-%m-%d')
t2 = f'{t1} 00:01:00.000'
period = int((datetime.datetime.strptime(t2, '%Y-%m-%d %H:%M:%S.%f')).timestamp() * 1000)

h = date_today.hour
day = 3
day_milli = day * 86400000
last_23h = int(time.time()*1000 - day_milli)# - 5184000000)#89600000)
last_hour = int(time.time()*1000 - 3600000)
r = time.ctime(last_hour)


def choose_time(name: str) -> float:
    if name != 'Profi':
        return last_23h
    else:
        return period


def record_offers(id: str) -> bool:
    """собираем айди офферов в lib.json и потом по нему проверям появление нового"""
    obj = bucket.get_object(bucket.auth())
    search_date = obj.get(t1, None)
    if search_date is not None:
        if id not in search_date:
            search_date.append(id)
            bucket.load_object(bucket.auth(), obj)
            return True
    else:
        obj[t1] = []
        bucket.load_object(bucket.auth(), obj)
        return False


def sale_back(dealer_id: int, name: str, session_id: str) -> str or None:
    start_from = choose_time(name)
    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': token,
        'Accept': 'application/json',
        'x-dealer-id': dealer_id,
    }
    data = {
        "pagination": {
            "page": 1,
            "page_size": 10
        },
        "filter": {
            "creation_date_from": start_from,
        },
        "only_last_seller": False,

    }
    r = requests.post(URL, json=data, headers=headers).json()
    print(r)
    text = ''
    try:
        for value in r['comebacks']:
            status = value['offer']['status']
            created = value['offer']['created']
            print(created)
            date = str(created).split('T')[0]
            if status == 'ACTIVE':
                mark = value['offer']['car_info']['mark']
                model = value['offer']['car_info']['model']
                url = value['offer']['mobile_url']
                offer_id = value['offer']['id']
                new_offer = record_offers(offer_id)
                if new_offer is True:
                    text += f'{name} {mark} {model}\n{url}\n'
            else:
                pass
        if len(text) > 0:
            print(text)
            return text
        else:
            return None
    except:
        pass

import datetime
from dotenv import load_dotenv

import os
import requests


load_dotenv()
token = os.getenv('MANAGER_TOKEN')
URL = 'https://apiauto.ru/1.0/comeback'
date_today = datetime.date.today()


def sale_back(dealer_id: int, name: str, session_id: str) -> str:
    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': token,
        'Accept': 'application/json',
        'x-dealer-id': dealer_id,
    }
    data = {
        "pagination": {
            "page": 1,
            "page_size": 5
        },
        "filter": {
            "creation_date_from": 0,
        },
        "only_last_seller": True,

    }
    r = requests.post(URL, json=data, headers=headers).json()
    try:
        offer_created = r['comebacks'][0]['offer']['created']
        date = str(offer_created).split('T')[0]
        if date == str(date_today):
            mark = r['comebacks'][0]['offer']['car_info']['mark']
            model = r['comebacks'][0]['offer']['car_info']['model']
            url = r['comebacks'][0]['offer']['mobile_url']
            text = f'{name} {mark} {model}\n{url} '
            return text
        else:
            pass
    except:
        pass

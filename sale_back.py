import datetime
from dotenv import load_dotenv
import os
import requests


load_dotenv()
token = os.getenv('MANAGER_TOKEN')
URL = 'https://apiauto.ru/1.0/comeback'
date_today = datetime.date.today()# - datetime.timedelta(days=1)


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
        "only_last_seller": False,

    }
    r = requests.post(URL, json=data, headers=headers).json()
    text = ''
    try:
        for value in r['comebacks']:
            created = value['offer']['created']
            date = str(created).split('T')[0]
            if date == str(date_today):
                mark = value['offer']['car_info']['mark']
                model = value['offer']['car_info']['model']
                url = value['offer']['mobile_url']
                text += f'{name} {mark} {model}\n{url}\n'
            else:
                pass
        return text
    except:
        pass

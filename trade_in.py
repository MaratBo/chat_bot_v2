from dotenv import load_dotenv
import os
import requests
import datetime


load_dotenv()
token = os.getenv('MANAGER_TOKEN')
date_today = datetime.date.today()
URL = 'https://apiauto.ru/1.0/dealer/trade-in'


def tradeIn_request(dealer_id: int, name: str, session_id: str) -> str or None:
    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': token,
        'Accept': 'application/json',
        'x-dealer-id': dealer_id,
    }
    data = {
        'from_date': date_today
        }

    r = requests.get(URL, params=data, headers=headers).json()
    try:
        all_requests = r.get('trade_in_requests')[0]
        seller_name = all_requests.get('user_info').get('name')
        seller_phone = all_requests.get('user_info').get('phone_number')
        offer = all_requests.get('client_offer').get('mobile_url')
        if seller_name is None:
            seller_name = 'Имя не указано '
        return f'кабинет {name}\nпользователь {seller_name} {seller_phone}\n{offer}\n'
    except:
        return None

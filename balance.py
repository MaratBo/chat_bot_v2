from dotenv import load_dotenv
import os
import requests


load_dotenv()
token = os.getenv('MANAGER_TOKEN')

URL = 'https://apiauto.ru/1.0/dealer/account'


def get_balance(dealer_id: int, name: str, session_id: str) -> str:
    """первый пуш менее 7 дней, второй 5 дней, третий если один день"""

    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': token,
        'Accept': 'application/json',
        'x-dealer-id': dealer_id,
    }

    r = requests.get(URL, headers=headers).json()

    try:
        days_to_empty = r['rest_days']

        if days_to_empty in [1, 3, 7]:
            text = f'{name}\nденьги закончатся через {days_to_empty} дн.\n'
            return text
    except:
        pass
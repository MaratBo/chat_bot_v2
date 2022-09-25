from dotenv import load_dotenv
import os
import requests
import datetime


load_dotenv()
token = os.getenv('MANAGER_TOKEN')
date_today = datetime.date.today()
URL = 'https://apiauto.ru/1.0/booking'


def online_booking(dealer_id: int, name: str, session_id: str) -> str or None:
    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': token,
        'Accept': 'application/json',
        'x-dealer-id': dealer_id,
    }

    r = requests.get(URL, headers=headers).json()

    try:
        all_bookings = r.get('bookings')[0]
        day_of_last_one = all_bookings.get('created_at').split('T')[0]
        if date_today == day_of_last_one:
            offer = all_bookings.get('offer')
            mark = offer.get('car_info').get('mark')
            model = offer.get('car_info').get('model')
            url = offer.get('mobile_url')
            return f'У вас новая бронь на {mark} {model}\n{url}'
        else:
            return None
    except:
        pass

import datetime
import json
import os
import requests
from time import sleep
from dotenv import load_dotenv
from customers import make_message
from balance import get_balance
from sale_back import sale_back
from custom_fit import artem_eremin
from access_archive import CABINET_ID, CHANNEL


load_dotenv()
token = os.getenv('MANAGER_TOKEN')
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
TLG_TOKEN = os.getenv('MARUSIA_TOKEN')


def get_session_id(name: str) -> str:
    global session_id
    url_session_id = "https://apiauto.ru/1.0/auth/login"
    payload = '{login:' + login + ', password: ' + password + '}'
    headers = {
        'x-authorization': token,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url_session_id, headers=headers, data=payload)
        session_id = json.loads(response.text.encode('utf8'))['session']['id']
    except KeyError or NameError:
        print(f"Сессия {name} не получена, проверьте логин или пароль.")
    return session_id


def script(dealer_id: int, name: str, name_group: str, session_id: str, group=False) -> list or None:
    """making message an answered and refused calls"""
    start_time = f'{datetime.date.today()}T00:00:00.000Z'
    headers = {
        'X-Session-Id': session_id,
        'X-Authorization': token,
        'Accept': 'application/json',
        'x-dealer-id': dealer_id,
    }

    data = {
        "pagination": {
            "page": 1,
            "page_size": 50},
        "filter": {
            "period":
                {
                    "from": start_time,
                }
        },
    }
    global target_calls
    if name_group in ['Avangard', 'Petrovsky', 'M2O', 'axis']:
        target_calls = 'уникальные/целевые'
        ADD_DATA = [{"targets": "ALL_TARGET_GROUP"}, {"targets": "TARGET_GROUP"}]
    else:
        target_calls = 'уникальные/пропущенные'
        ADD_DATA = [{"results": "ALL_RESULT_GROUP"}, {'results': 'MISSED_GROUP'}]
    global send_data
    send_data = []
    for i in ADD_DATA:
        data['filter'].update(i)
        URL = 'https://apiauto.ru/1.0/calltracking'
        r = requests.post(URL, json=data, headers=headers).json()
        try:
            unic_calls = set((map(lambda x: x['source']['raw'], r['calls'])))
            send_data.append(len(unic_calls))
        except:
            send_data.append(0)
    if send_data[0] != 0:
        text = make_message(name_group, name, send_data)
        if name_group in ['geely_planeta', 'used_planeta', 'chery_planeta', 'skoda_planeta']:
            custom_message = artem_eremin(dealer_id, session_id)
            return f'{text[0]}\n{custom_message}'
        else:
            if group is True:
                return text
            else:
                return text[0]
    else:
        return None


def message(sms, CHAT_ID):
    URL = (
        'https://api.telegram.org/bot{token}/sendMessage'.format(token=TLG_TOKEN))
    data = {'chat_id': CHAT_ID,
            'text': sms
            }
    requests.post(URL, data=data)
    #print(sms)


def collect_data() -> None:
    with open("info/id_cab.json", "r") as id_file:
        data = json.load(id_file)
    #access = data['CABINET_ID2']
    access = CABINET_ID
    # chat_adress = data['CHANNEL']
    chat_adress = CHANNEL[0]
    time = datetime.date.today().strftime('%d.%m')
    for value in access:
        dealer_name = list(value)[0]
        chat_id = chat_adress[dealer_name]
        session_id = get_session_id(dealer_name)
        if len(value[dealer_name]) == 1:
            calls_info = script(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'), dealer_name,
                                session_id)
            if calls_info is not None:
                message(f'Звонки за {time} {target_calls}\n'
                        f'{calls_info}', chat_id)
            balance_info = get_balance(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'), session_id)
            if balance_info is not None:
                message(f'Балансы кабинетов:\n{balance_info}', chat_id)
            my_excar = sale_back(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'), session_id)
            if my_excar is not None:
                message(f'Ваш автомобиль снова в продаже:\n{my_excar}', chat_id)
        else:
            calls_text = ''
            balance_text = ''
            my_ex_text = ''
            for avtosalon in value[dealer_name]:
                calls_info = script(avtosalon.get('id'), avtosalon.get('name'), dealer_name, session_id, group=True)
                balance_info = get_balance(avtosalon.get('id'), avtosalon.get('name'), session_id)
                my_excar = sale_back(avtosalon.get('id'), avtosalon.get('name'), session_id)
                if calls_info is not None:
                    calls_text += f'{calls_info[-1]}\n'
                if balance_info is not None:
                    balance_text += balance_info
                if my_excar is not None:
                    my_ex_text += f'{my_excar}\n'
            if calls_text != '':
                message(f'Звонки за {time} {target_calls}\n'
                        f'{calls_text}', chat_id)
            if balance_text != '':
                message(f'Балансы кабинетов:\n{balance_text}', chat_id)
            if my_ex_text != '':
                message(f'Ваш автомобиль снова в продаже:\n{my_ex_text}', chat_id)


if __name__ == '__main__':
    while True:
        time_now = datetime.datetime.now() + datetime.timedelta(hours=3)
        h = time_now.hour
        m = time_now.minute
        d = time_now.date().strftime("%d")
        print(f'check time {h}:{m}')
        if m in range(0, 59) and h == 21:
            print(f'start script {d}-{h}:{m}')
            collect_data()
            sleep(84600)
        else:
            sleep(1200)

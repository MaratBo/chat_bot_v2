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
from access_archive import CABINET_ID_18, CHANNEL, CABINET_MORNING, CABINET_ID_12, TEST_TIME, REGINAS
from booking import online_booking
from trade_in import tradeIn_request



token = os.environ.get('MANAGER_TOKEN')
login = os.environ.get('LOGIN')
password = os.environ.get('PASSWORD')
TLG_TOKEN = os.environ.get('MARUSIA_TOKEN')


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
    end_time = None
    if name_group == "ACLeninsky":
        start_time = f'{datetime.date.today() - datetime.timedelta(days=1)}T00:00:00.000Z'
        end_time = f'{datetime.date.today() - datetime.timedelta(days=1)}T23:59:59.000Z'
    else:
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
                    "to": end_time
                }
        },
    }
    global target_calls
    if name_group in ['Avangard', 'Petrovsky', 'M2O', 'axis', 'Avtopark', 'ACLeninsky',]:
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
    #requests.post(URL, data=data)
    print(sms)


def collect_data(cabinet_list) -> None:
    access = cabinet_list
    channel_list = CHANNEL[0]
    time = datetime.date.today().strftime('%d.%m')
    yesterday = (datetime.date.today() - datetime.timedelta(days=0)).strftime('%d.%m')
    for value in access:
        dealer_name = list(value)[0]
        chat_id = channel_list[dealer_name][0]
        processing_permissions = channel_list[dealer_name][1]
        try:
            session_id = get_session_id(dealer_name)
        except:
            print(value, ' no session_id')
        if len(value[dealer_name]) == 1:
            if processing_permissions['calls'] is True:
                calls_info = script(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'), dealer_name,
                                    session_id)
                if calls_info is not None and dealer_name in ['ACLeninsky',]:
                    message(f'Звонки за {yesterday} {target_calls}\n'
                            f'{calls_info}', chat_id)
                elif calls_info is not None:
                    message(f'Звонки за {yesterday} {target_calls}\n'
                            f'{calls_info}', chat_id)
            if processing_permissions['balance'] is True:
                balance_info = get_balance(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'),
                                           session_id)
                if balance_info is not None:
                    message(f'Балансы кабинетов:\n{balance_info}', chat_id)
            if processing_permissions['my_ex'] is True:
                my_excar = sale_back(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'), session_id)
                #print(f'my ex get back {my_excar}')
                if my_excar is not None:
                   # print(f'sms {my_excar}')
                    message(f'Ваш автомобиль снова в продаже:\n{my_excar}', chat_id)
            if processing_permissions['booking'] is True:
                booking_car = online_booking(value[dealer_name][0].get('id'), value[dealer_name][0].get('name'),
                                             session_id)
                if booking_car is not None:
                    message(booking_car, chat_id)
            if processing_permissions['trade-in'] is True:
                trade_in_requests = tradeIn_request(value[dealer_name][0].get('id'),
                                                    value[dealer_name][0].get('name'),
                                                    session_id)
                if trade_in_requests is not None:
                    message(f'Новая заявка на трейд-ин:\n{trade_in_requests}', chat_id)
        else:
            calls_text = ''
            balance_text = ''
            my_ex_text = ''
            booking_text = ''
            trade_in_text = ''
            for avtosalon in value[dealer_name]:
                if processing_permissions['calls'] is True:
                    calls_info = script(avtosalon.get('id'), avtosalon.get('name'), dealer_name, session_id,
                                        group=True)
                    if calls_info is not None:
                        calls_text += f'{calls_info[-1]}\n'
                if processing_permissions['balance'] is True:
                    balance_info = get_balance(avtosalon.get('id'), avtosalon.get('name'), session_id)
                    if balance_info is not None:
                        balance_text += balance_info
                if processing_permissions['my_ex'] is True:
                    #print(f'my ex text TRUE {my_ex_text}')
                    my_excar = sale_back(avtosalon.get('id'), avtosalon.get('name'), session_id)
                    if my_excar is not None:
                        #print(my_excar)
                        my_ex_text += f'{my_excar}'
                if processing_permissions['booking'] is True:
                    booking_car = online_booking(avtosalon.get('id'), avtosalon.get('name'), session_id)
                    if booking_car is not None:
                        booking_text += f'{booking_car}\n'
                if processing_permissions['trade-in'] is True:
                    trade_in_requests = tradeIn_request(avtosalon.get('id'), avtosalon.get('name'), session_id)
                    if trade_in_requests is not None:
                        trade_in_text += f'{trade_in_requests}\n'
            if calls_text != '' and dealer_name in ['ACLeninsky']:
                message(f'Звонки за {yesterday} {target_calls}\n'
                        f'{calls_text}', chat_id)
            elif calls_text != '':
                message(f'Звонки за {time} {target_calls}\n'
                        f'{calls_text}', chat_id)
            if balance_text != '':
                message(f'Балансы кабинетов:\n{balance_text}', chat_id)
            #print(f'my ex text {my_ex_text}')
            if my_ex_text != '':
                message(f'Ваши автомобили снова в продаже (за 60 дней):\n{my_ex_text}', chat_id)
            if booking_text != '':
                message(booking_text, chat_id)
            if trade_in_text != '':
                message(f'Новая заявка на трейд-ин:\n{trade_in_text}', chat_id)


# def test_new_channel():
#     sms = 'test'
#     ids = ['@reginas_lenina']
#     for id in ids:
#         print(sms, id)
#         message(sms, id)
#
# test_new_channel()

def reginas():
    collect_data(REGINAS)
reginas()

#
# if __name__ == '__main__':
#     time_now = datetime.datetime.now()
#     h = time_now.hour
#     m = time_now.minute
#     print(f'check time {h}:{m}')
#     if h == 8:
#         collect_data(CABINET_MORNING)
#     elif h == 9:
#         collect_data(CABINET_ID_12)
#     elif h == 16:
#         collect_data(TEST_TIME)
#     else:
#         collect_data(CABINET_ID_18)




import requests
from time import sleep
import base64
from endpoints import SERVER_URL
from env import DEBUG, CHANNEL1, CHANNEL2
import os
import logging


if DEBUG:
    CHANNEL1 = "o13srdbtydg55Sjc3h_testing"
    CHANNEL2 = "xhoxnvpun6lvjj23er_debug"


def send_to_ntfy(message):
    url = SERVER_URL + message['Type'].lower()
    token = os.getenv('MAINSTREAM_TOKEN')
    if DEBUG:
        url = SERVER_URL + CHANNEL1
        token = os.getenv('TESTING_TOKEN')

    try:
        more_headers = beautify_message(message['Subject'].strip())

        headers={
                "Authorization": f'Bearer {token}',
                "Title": message['Title'].strip(),
                "Message": encode_rfc_2047_base64(message['body']),
                "Tags": more_headers['Tags'],
                "Priority": more_headers['Priority'],
                # "Icon": more_headers['Icon'],
            }

        if 'attachment' in message:
            headers["Filename"] = "notice.pdf"
            details = requests.put(url,
                data=message['attachment'],
                headers=headers
            )
        else:
            details = requests.put(url,
                headers=headers
            )

        details.raise_for_status()


    except Exception as e:
        logging.error(f" Failed to Send Notice3 : {message['Subject']} ~ {str(e)}")
        message['Title'] = f" Failed to Send : {message['Title']}"
        error_ntfy(message)


def schedule_ntfy(message):
    url = SERVER_URL + message['Type'].lower()
    token = os.getenv('MAINSTREAM_TOKEN')
    if DEBUG:
        url = SERVER_URL + CHANNEL1
        token = os.getenv('TESTING_TOKEN')

    try:
        headers={
                "Authorization": f'Bearer {token}',
                "Title": message['Title'].strip(),
                "Message": encode_rfc_2047_base64(message['body']),
                "Tags": 'hourglass_flowing_sand,bell',
                "Priority": '4',
                'Delay': message['Delay'],
                # "Icon": more_headers['Icon'],
            }

        if 'attachment' in message:
            headers["Filename"] = "notice.pdf"
            details = requests.put(url,
                data=message['attachment'],
                headers=headers
            )
            
        else:
            details = requests.put(url,
                headers=headers
            )
        details.raise_for_status()

    except Exception as e:
        logging.error(f" Failed to Send Notice3 : {message['Subject']} ~ {str(e)}")
        message['Title'] = f" Failed to Schedule : {message['Title']}"
        error_ntfy(message)


## NO ERROR ZONE EXPLICITY CHECK
def error_ntfy(message):
    url = SERVER_URL + CHANNEL2
    token = os.getenv('ERROR_TOKEN')
    if DEBUG:
        url = SERVER_URL + CHANNEL2
        token = os.getenv('DEBUG_TOKEN')

    try:
        details = requests.put(f"{url}",
            data="There is an error in sending the notice please check the notice board",
            headers={
                "Authorization": f'Bearer {token}',
                "Title": encode_rfc_2047_base64(message['Title'].strip()), #remove whitespace error
                "Tags": "warning,lady_beetle",
                "Priority": "5",
                # "Icon": "https://styles.redditmedia.com/t5_32uhe/styles/communityIcon_xnt6chtnr2j21.png",
                }
            )
        details.raise_for_status()

    except Exception as e:
        logging.error(f" Failed to Send Notice4 : {message['Subject']} ~ {str(e)}")
        sleep(120)

        try:
            details = requests.put(f"{url}",
                data="There is an error in sending the notice please check the notice board",
                headers={
                    "Authorization": f'Bearer {token}',
                    "Title": encode_rfc_2047_base64(message['Title'].strip()), #remove whitespace error
                    "Tags": "warning,lady_beetle",
                    "Priority": "5",
                    # "Icon": "https://styles.redditmedia.com/t5_32uhe/styles/communityIcon_xnt6chtnr2j21.png",
                    }
                )
            details.raise_for_status()

        except Exception as e:
            logging.error(f" Failed to Send Notice5 : {message['Subject']} ~ {str(e)}")



def beautify_message(subject):
    headers = {}
    if subject == 'PPO':
        headers['Priority'] = '3'
        headers['Tags'] = 'love_letter'
        headers['Icon'] = '❤️'

    elif subject == 'Urgent':
        headers['Priority'] = '5'
        headers['Tags'] = 'exclamation, stop_sign'
        headers['Icon'] = '🚨'

    elif subject == 'PPT/Workshop/Seminars etc':
        headers['Priority'] = '2'
        headers['Tags'] = 'popcorn'
        headers['Icon'] = '📊'

    elif subject == 'Result':
        headers['Priority'] = '4'
        headers['Tags'] = 'bowing_man,cup_with_straw'
        headers['Icon'] = '✅'

    elif subject == 'Schedule':
        headers['Priority'] = '5'
        headers['Tags'] = 'calendar'
        headers['Icon'] = '📅'

    elif subject == 'CV Submission':
        headers['Priority'] = '5'
        headers['Tags'] = 'briefcase'
        headers['Icon'] = '📄'

    elif subject == 'Shortlist':
        headers['Priority'] = '5'
        headers['Tags'] = 'chart_with_upwards_trend'
        headers['Icon'] = '📋'
    
    elif subject == 'Postponement':
        headers['Priority'] = '5'
        headers['Tags'] = 'alarm_clock,arrow_forward'
        headers['Icon'] = 'ℹ️'


    else:
        headers['Priority'] = '5'
        headers['Tags'] = 'arrow_forward'
        headers['Icon'] = 'ℹ️'

    return headers


def encode_rfc_2047_base64(input_string):
    # Encode the input string to bytes using UTF-8 and then to Base64
    base64_encoded = base64.b64encode(input_string.encode('utf-8')).decode('ascii')

    # Format the RFC 2047 string
    rfc2047_encoded = f'=?UTF-8?B?{base64_encoded}?='

    return rfc2047_encoded

# def raise_error(message="An error occurred"):
#     raise Exception(message)

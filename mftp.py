import env
import mailcopy as mail
import time
import notice
import requests
import argparse
import random
from datetime import datetime
import iitkgp_erp_login.erp as erp
import logging

global_var = 1

def run_hold_session():
    global_var = global_var + 1 
    # Set up a loop to make the request periodically
    while not(global_var % 27):
        
        # Make the request after the delay
        url = "https://erp.iitkgp.ac.in/IIT_ERP3/holdSession.htm?rand_id="

        with open(".session", 'r') as file:
            jsid = file.readline()
            ssotoken = file.readline()

            headers = {
            # 'Accept': 'application/xml, text/xml, */*; q=0.01',
            # 'Accept-Language': 'en-GB,en;q=0.5',
            # 'Connection': 'keep-alive',
            'Cookie': f'ssoToken={ssotoken}; JSID#/TrainingPlacementSSO={jsid}',
            'Referer': 'https://erp.iitkgp.ac.in/TrainingPlacementSSO/TPStudent.jsp',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            # 'Sec-GPC': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            # 'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Brave";v="120"',
            # 'sec-ch-ua-mobile': '?0',
            # 'sec-ch-ua-platform': '"macOS"'
            }

            random_int = str(random.randint(10**14, (10**15)-1))
            # print(random_int)
            response = requests.get(url+random_int, headers=headers)
            # Check the response

            if response.text == "SUCCESS":
                logging.info(f"Session hold request successful")
            else:
                # print(f"Session hold request failed with status code: {response.status_code}")
                logging.error(f" Request failed : {response.status_code} and response \n{response.text}\n" )
                

            global_var = 1

    
lsnif = "lsnif"
headers = {
    'timeout': '20',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
}
session = requests.Session()

parser = argparse.ArgumentParser(description='One stop mailing solution for CDC NoticeBoard at IIT KGP')
parser.add_argument('--smtp', action="store_true", help='Use SMTP for sending the mails', required=False)
parser.add_argument('--gmail-api', action="store_true", help='Use GMAIL API for sending the mails', required=False)
args = parser.parse_args()



while True:
    print(f"================ <<: {datetime.now()} :>> ================", flush=True)
    print('[ERP LOGIN]', flush=True)
    _, ssoToken = erp.login(headers, session, ERPCREDS=env, OTP_CHECK_INTERVAL=2, LOGGING=True, SESSION_STORAGE_FILE='.session')
    
    notices = notice.fetch(headers, session, ssoToken, lsnif)
    mails = mail.format_notice(notices, session)
    mail.send(mails, lsnif, notices)
    
    print("[PAUSED FOR 2 MINUTES]", flush=True)
    time.sleep(60)
    run_hold_session()
    time.sleep(60)
    run_hold_session()

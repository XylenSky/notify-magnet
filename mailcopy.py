import re
import logging
from ntfy import send_to_ntfy, error_ntfy, schedule_ntfy
from bs4 import BeautifulSoup as bs
from endpoints import NOTICE_CONTENT_URL, ATTACHMENT_URL
from notice import update_lsni, get_latest_index
import ntfy
import dateutil.parser
import datetime
import copy
from time import sleep


def send(mails, smtp, gmail_api, lsnif, notices):
    if mails: 
        print(f"[SENDING MAILS]", flush=True)
        for i, mail in enumerate(mails, 1):
            if has_idx_mutated(lsnif, notices, i):
                logging.error(f" Mutated index found ~ {i}")
                # break

            try:
                send_to_ntfy(mail)
                logging.info(f" [MAIL SENT] ~ {mail['Subject']}")
                update_lsni(lsnif, notices, i)
            except Exception as e:
                logging.error(f" Failed to Send Mail1 : {mail['Subject']} ~ {str(e)}")
                mail['Title'] = f" Failed to Send Notice : {mail['Title']}"
                error_ntfy(mail)
            sleep(.1)


def format_notice(notices, session):
    if notices: print('[FORMATTING MAILS]', flush=True)

    mails = []
    i = 0
    for notice in (notices):
        id_, year = notice['UID'].split('_')
        message = {}
        message['Type'] = notice['Type']
        message['Subject'] = notice['Subject']
        message["Title"] = f"#{id_} | {notice['Subject']} | {notice['Company']}"
        
        try:
            body = parseBody(session, year, id_)
        except Exception as e:
            logging.error(f" Failed to parse mail body ~ {str(e)}")
            message['Title'] = f"Failed to Send : {message['Subject']}"
            error_ntfy(message)
            continue

        lines = body.split('\n')  # Split the text into lines
        # Take a slice starting from the fourth line
        cleaned_text = '\n'.join(lines[6:])
        processed_text = '\n'+cleaned_text+'\n'


        body =  cleaned_text.rstrip() + '                ' + re.sub(r'\s+', ' ', notice['Time'])
        
        message['body']=body

        
        # Handling attachment
        try:
            attachment = parseAttachment(session, year, id_)
            if len(attachment) == 0 and ('Please find attached' in processed_text or 'PFA' in processed_text):
                z = 0
                while len(attachment) == 0 and z < 3:
                    sleep(30)
                    attachment = parseAttachment(session, year, id_)
                    z = z + 1
                logging.info(f" Waited till to parse mail attachment ~ {z}")

        except Exception as e:
            logging.error(f" Failed to parse mail attachment ~ {str(e)}")
            message['Title'] = f" Failed to Send : {message['Title']}"
            error_ntfy(message)
            continue

        if len(attachment) != 0:
            message['attachment'] = attachment
            logging.info(f" [PDF ATTACHED] On notice #{id_} of length ~ {len(attachment)}")


        if notice['Subject'].strip() not in ['PPO', 'Result']: # No reminders for the PPO and Result
            message_remainder = copy.deepcopy(message)
            try:
                dates = extract_date_time_formats(processed_text.replace('noon','PM'))
                # print('message data', dates)
                if dates:
                    message['body'] += '\n'
                    dates = sorted(dates)
                    logging.info(f" Dates parsed On notice #{id_} ~ {dates}")
                for date in dates:
                    date_for_rem = date - datetime.timedelta(minutes=30)
                    remainder_date = int(datetime.datetime.timestamp(date_for_rem))

                    if date - datetime.timedelta(hours=12) > datetime.datetime.now():
                        message_remainder['Title'] = "Remainder "+ date.strftime("%I:%M %p")+" for Notice"+ message['Title']
                        message_remainder['Delay'] = f'{remainder_date}'
                        try:
                            # schedule_ntfy(message_remainder)
                            human_readable_format = "%A, %d %b %Y at %I:%M %p IST"
                            message['body'] +=  f'\nRemainder is set for {date.strftime(human_readable_format)}'
                            logging.info(f" Remainder is set for the date for notice #{id_} ~ {date.strftime(human_readable_format)}")
                        except Exception as e:
                            message['body'] += '\nSetting a Reaminder for {date} is failed'
                            logging.error(f" Failed to set the remainder ~ {str(e)}")
                            
            except Exception as e:
                message['body'] += '\n\nSetting a Remainder for any date is failed'
                logging.error(f" Failed to set the remainder ~ {str(e)}")
                # continue // not required not necessary element of original message
            
        mails.append(message)

    return mails


def has_idx_mutated(lsnif, notices, i):
    lidx_from_file = get_latest_index(lsnif) # Latest Index from File
    cidx_from_to_send_mails = int(notices[-i]['UID'].split('_')[0]) # Current Index from to send mails
    difference_in_idx = cidx_from_to_send_mails - lidx_from_file

    if difference_in_idx != 1: 
        logging.error(f" Trying to send mail #{cidx_from_to_send_mails} while latest in database is #{lidx_from_file}")
        mail = {}
        mail['Subject'] = 'Missing Notice'
        mail["Title"] = f"#{lidx_from_file+1} | {mail['Subject']}"
        mail['body'] = 'Notice not found or missing'
        error_ntfy(mail)
        return True
    
    return False


def parseBody(session, year, id_):
    content = session.get(NOTICE_CONTENT_URL.format(year, id_))
    content_html = bs(content.text, 'html.parser')
    content_html_div = bs.find_all(content_html, 'div', {'id': 'printableArea'})[0]
    body = content_html_div.decode_contents(formatter='html')

    soup = bs(body, 'html.parser')

    # Convert the soup to string with appropriate formatting
    body = soup.get_text(separator='\n', strip=True)

    return body


def parseAttachment(session, year, id_):
    stream = session.get(ATTACHMENT_URL.format(year, id_), stream=True)
    attachment = b''
    for chunk in stream.iter_content(4096):
        attachment += chunk
    
    return attachment
    

def extract_date_time_formats(text):
    # Define a regular expression pattern to match various date and time formats
    with open('regex_pattern_date.txt', 'r') as file:
        pattern = file.read()

    matches = re.findall(pattern, text)

    extracted_formats = [value for match in matches for value in match if value]
    dates = []
    for date in extracted_formats:
        try:
            dates.append(dateutil.parser.parse(date, dayfirst=True))
        except ValueError:
            try:
                dates.append(extra_date_parser(date))
            except ValueError:
                logging.error(f" This date parser need to be added ~ {date}")
                continue

    extracted_formats = set(dates)
    unique_dates = list(extracted_formats)

    # print(unique_dates, flush=True)

    return unique_dates


def extra_date_parser(date_str):
    """
    Parses a date string using a list of possible date formats.

    Args:
        date_str (str): The date string to be parsed.

    Returns:
        datetime: A datetime object representing the parsed date and time.

    Raises:
        ValueError: If the date string cannot be parsed with any of the specified formats.
    """
    date_formats = [
        "%d.%m.%Y, %I.%M %p",
        # "%m/%d/%Y, %I.%M %p",
        # "%Y-%m-%d, %H:%M:%S",
        "%dth %B %Y, %I.%M %p"
    ]

    parsed_date = None

    for format in date_formats:
        try:
            parsed_date = datetime.datetime.strptime(date_str, format)
            break  # If parsing succeeds, exit the loop
        except ValueError:
            continue  # If parsing fails, try the next format

    if parsed_date:
        return parsed_date
    else:
        raise ValueError("Unable to parse the date")

def raise_error(message="An error occurred"):
    raise Exception(message)

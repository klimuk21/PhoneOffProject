import datetime
import email
import imaplib
import re

def collector():
    EMAIL_ACCOUNT = "klimuk.alex21@gmail.com"
    PASSWORD = "reddevil95"

    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('inbox')

    # (ALL/UNSEEN - выборка) за последний день (параметр timedelta)
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    result, data = mail.uid('search', None, '(SENTSINCE {date} HEADER Subject "PHONEOFF")'.format(date=date))
    i = len(data[0].split())

    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')

        # result, email_data = conn.store(num,'-FLAGS','\\Seen')
        # Можно установить флаг письма в просмотрено.

        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')
        email_message = email.message_from_string(raw_email_string)

        # Header Details
        # date_tuple = email.utils.parsedate_tz(email_message['Date'])
        # if date_tuple:
        # local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        # local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))

        # email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        # email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        # subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
        # таким образом можно считывать детали письма


        # Body details
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                file_name = "email_" + str(x) + ".txt"
                output_file = open(file_name, 'w')
                output_file.write((body.decode('utf-8')))
                output_file.close()
                # парсим
                f = open(file_name, 'r')
                msisdns = f.read()
                msisdns = re.findall(r'375[0-9]{9}', str(msisdns))
                stroka = '\n'.join(msisdns)
                print(stroka)
                f.close()
                f = open(file_name, 'w')
                f.write(stroka)
                f.close()

            else:
                continue
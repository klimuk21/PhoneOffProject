import smtplib
import fnmatch
import os

def send_alert(subject, text):

    to = ['akl@bamboogroup.eu']
    gmail_user = 'klimuk.alex21@gmail.com'
    gmail_pwd = 'reddevil95'
    smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + ", ".join(to) + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: ' + subject + '\n'
    msg = header + '\n' + text + '\n\n'
    smtpserver.sendmail(gmail_user, to, msg)

    smtpserver.close()


def sending_mess():
    subject = 'PHONEOFF'

    for file in os.listdir('.'):  #пробегаем по файлам с номерами
        if fnmatch.fnmatch(file, '*.txt'):
            print(file)
            output_file = open(file, 'r')
            msisdns = output_file.read()
            send_alert(subject, msisdns)
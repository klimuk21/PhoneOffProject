# -----------local connect

from __future__ import print_function
import pymysql.cursors
import re
import os
import fnmatch
import glob

def get_connection_blacklist():
    connection = pymysql.connect(
        host='localhost',
        user='debian-sys-maint',
        password='2080085',
        db='blacklist',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    return connection

def get_connection_broadcaster_by():
    connection = pymysql.connect(
        host='localhost',
        user='debian-sys-maint',
        password='2080085',
        db='broadcaster_by',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    return connection

def get_connection_football_hero():
    connection = pymysql.connect(
        host='localhost',
        user='debian-sys-maint',
        password='2080085',
        db='football_hero',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )
    return connection

def request_to_db_blacklist(request):
    connection: pymysql.connections.Connection = get_connection_blacklist()

    try:
        with connection.cursor() as cursor:
            cursor.execute(request)
            print(request)
            return cursor

    finally:
        connection.close()

def request_to_db_broadcaster_by(request):
    connection: pymysql.connections.Connection = get_connection_broadcaster_by()

    try:
        with connection.cursor() as cursor:
            cursor.execute(request)
            print(request)
            return cursor

    finally:
        connection.close()

def request_to_db_football_hero(request):
    connection: pymysql.connections.Connection = get_connection_football_hero()

    try:
        with connection.cursor() as cursor:
            cursor.execute(request)
            print(request)
            return cursor

    finally:
        connection.close()


def request():
    for file in os.listdir('.'):  #пробегаем по файлам с номерами
        if fnmatch.fnmatch(file, '*.txt'):
            print(file)
            output_file = open(file, 'r')
            msisdns = output_file.read()

            msisdns = re.findall(r'375[0-9]{9}', str(msisdns)) #парсим
            stroka = ', '.join(msisdns) #добавляем запятую
            print(stroka)
            # выполняем запросы
            request_to_db_blacklist(f"UPDATE `blacklist`.`msisdns` SET `lifetime` = '0' WHERE `msisdn` in (SELECT `msisdn` WHERE msisdn IN ({stroka}) AND lifetime > '259200');")

            request_to_db_broadcaster_by(f"UPDATE `broadcaster_by`.`subscribers` SET `stopped` = '1', stop_time = now() WHERE `msisdn` in (SELECT msisdn WHERE msisdn IN ({stroka}) AND (activated = '1' AND stopped = '0'));")

            request_to_db_football_hero(f"UPDATE `football_hero`.`subscriptions` SET `is_active` = '0', `is_deleted` = '1', `deleted_at` = now() WHERE `msisdn` in (SELECT msisdn WHERE msisdn IN ({stroka}) AND (`is_active` = '1' AND `is_deleted` = '0'));")

            output_file.close()

    files = glob.glob('*.txt') #удаляем файлы с номерами
    for f in files:
        os.remove(f)
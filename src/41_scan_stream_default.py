#!/usr/bin/python3

import os
import cv2
import time
import sys
import requests
import socket
from multiprocessing import Pool
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")

HTTP_AUTH_USER = os.getenv("HTTP_AUTH_USER", "admin")
HTTP_AUTH_PASS = os.getenv("HTTP_AUTH_PASS", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    sys.exit("Error: DB_USER, DB_PASSWORD or DB_NAME are missing in .env")

HOST_IP = socket.gethostbyname(socket.gethostname())

engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")


def select_ip_list():
    query = text("""
        SELECT `ip`, CONCAT(REPLACE(`ip`,'.','_'), '-' , `country_code`, '-', `region`, '-', `city`) as 'name_camera'
        FROM rtsp_scan
        WHERE `url` IS NULL AND `up` = :uname
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"uname": os.uname()[1]})
        return result.fetchall()


def get_link_list():
    query = text("SELECT `path`, `login`, `passwd` FROM `view_support_path_default`")
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()


def insert_url(link_one, ip, link, login, passwd):
    query = text("""
        UPDATE `rtsp_scan`
        SET `url` = :link_one, `up` = :uname, `link` = :link, `login` = :login, `passwd` = :passwd
        WHERE `ip` = :ip
    """)
    params = {
        "link_one": link_one,
        "uname": os.uname()[1],
        "link": link,
        "login": login,
        "passwd": passwd,
        "ip": ip
    }
    with engine.connect() as conn:
        conn.execute(query, params)
        conn.commit()


def job(ip):
    try:
        cap = cv2.VideoCapture(ip[0])
        ret, frame = cap.read()
        cap.release()

        if ret:
            print(ip)
            name_file = f"/var/www/html/scan/{ip[2]}.jpg"

            auth_str = f"{HTTP_AUTH_USER}:{HTTP_AUTH_PASS}@" if HTTP_AUTH_PASS else ""
            url_link = f"http://{auth_str}{HOST_IP}/scan/{ip[2]}.jpg"

            cv2.imwrite(name_file, frame)
            insert_url(ip[0], ip[1], url_link, ip[3], ip[4])
    except Exception as e:
        return


def main():
    link_list = get_link_list()

    for link in link_list:
        rtsp_list = []
        for ip in select_ip_list():
            rtsp_list.append([link[0].replace('ip_for_replace', ip[0]), ip[0], ip[1], link[1], link[2]])

        start = time.time()
        with Pool(processes=200) as p:
            p.map(job, rtsp_list)

        print("And start sleep")
        end = time.time()
        sl_tm = 300 - int(end - start)
        print(sl_tm)
        if sl_tm > 0:
            time.sleep(sl_tm)


def notify_telegram(duration):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram notification skipped: TOKEN or CHAT_ID missing.")
        return

    send_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': f"41_scan_stream_default done - {int(duration)}"
    }

    try:
        requests.post(send_url, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram notification: {e}")


if __name__ == "__main__":
    start_time = time.time()
    main()
    done = time.time() - start_time

    notify_telegram(done)

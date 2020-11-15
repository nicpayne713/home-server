import datetime
import logging
import os
import sqlite3 as sl

con = sl.connect('records.sqlite3')

SQL = 'INSERT INTO SPEEDS (timestamp, download, upload, ping) VALUES (?,?,?,?)'
SPEEDTEST_CMD = os.environ.get('SPEEDTEST_CMD')
LOG_FILE = 'speedtest.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M", )


def make_db():
    with con:
        con.execute("""
        CREATE TABLE SPEEDS (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME,
            download NUMERIC,
            upload NUMERIC,
            ping NUMERIC
        );
        """)


def main():

    # get data
    try:
        ping, download, upload = get_ping_results()
        # logging.info("%5.2f %5.2f %5.2f", ping, download, upload)
    except ValueError as err:
        logging.info(err)
        return None

    # append to db
    with con:
        con.execute(SQL, [datetime.datetime.now(), download, upload, ping])


def get_ping_results():
    ping = download = upload = None

    with os.popen(SPEEDTEST_CMD + ' --simple') as speedtest_output:
        for line in speedtest_output:
            label, value, unit = line.split()
            if 'Ping' in label:
                ping = float(value)
            elif 'Download' in label:
                download = float(value)
            elif 'Upload' in label:
                upload = float(value)

    if all((ping, download, upload)):
        return ping, download, upload
    else:
        raise ValueError('TEST FAILED')


if __name__ == '__main__':
    import time
    try:
        make_db()
    except:
        pass

    for _ in range(5):
        main()



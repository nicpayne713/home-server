import logging
import os
import sqlite3 as sl
import datetime
import pandas as pd
import plotly.express as px


con = sl.connect('records.sqlite3')

SQL = 'INSERT INTO SPEEDS (timestamp, download, upload, ping) VALUES (?,?,?,?)'
# os.environ['SPEEDTEST_CMD'] = r'C:\ProgramData\Miniconda3\envs\home-server-env\Scripts\speedtest-cli'
SPEEDTEST_CMD = os.environ.get('SPEEDTEST_CMD')
LOG_FILE = 'speedtest.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                        format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M", )


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


def read_data():
    df = pd.read_sql(
        """SELECT * FROM SPEEDS""", con
    )

    return df


# def create_plot(df):
#     plot_file_name = 'bandwidth.png'
#     rcParams['xtick.labelsize'] = 'xx-small'
#
#     plt.plot(df['timestamp'], df['download'], 'b-')
#     plt.title('1519 W.Taylor St Xfinity Bandwidth Report')
#     plt.ylabel('Bandwidth in MBps')
#     plt.yticks(range(0, 401, 20))
#     plt.ylim(0.0, 400.0)
#
#     plt.xlabel('Date/Time')
#     plt.xticks(rotation='45')
#
#     plt.grid()
#
#     current_axes = plt.gca()
#     current_figure = plt.gcf()
#
#     hfmt = dates.DateFormatter('%m/%d %H:%M:%S')
#     current_axes.xaxis.set_major_formatter(hfmt)
#     current_figure.subplots_adjust(bottom=.25)
#
#     loc = current_axes.xaxis.get_major_locator()
#     loc.maxticks[dates.HOURLY] = 24
#     loc.maxticks[dates.MINUTELY] = 60
#
#     current_figure.savefig(plot_file_name)
#     current_figure.show()


if __name__ == '__main__':
    import time
    make_db()
    while True:
        main()
        time.sleep(30)  # get measurement every 2 minutes

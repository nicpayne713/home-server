
import sqlite3 as sl
import pandas as pd
import plotly.express as px


def make_fig():
    con = sl.connect('src/records.sqlite3')

    df = pd.read_sql_query("select * from speeds;", con)

    fig = px.line(df, x='timestamp', y=['download', 'upload', 'ping'])
    fig.write_image("./docs/speetest_res.jpeg")


if __name__ == '__main__':
    make_fig()

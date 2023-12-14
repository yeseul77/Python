import requests
import pandas as pd
import pymysql


def get_df(url):
    api_key = '494e45546661707037397647657252'
    url_re = url.replace('(인증키)', api_key).replace('xml', 'json').replace('/5/', '/1000/')
    res = requests.get(url_re).json()
    df = pd.DataFrame(res[url.split('/')[-4]]['row'])
    return df


def connect_mysql(db='icia_test'):
    conn = pymysql.connect(host='localhost', port=3306,
                           user='root', password='3460',
                           db=db, charset='utf8')
    return conn


def sql_execute(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def sql_execute_dict(conn, query):
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(query)
    result = cursor.fetchall()
    return result

import requests
import pandas as pd
import pymysql
import random
from tqdm import tqdm
import time

api_key = 'RGAPI-3e834f86-cece-4e8a-9399-3b8110fcbe60'
seoul_api_key = '494e45546661707037397647657252'


def get_df(url):
    url_re = url.replace('(인증키)', seoul_api_key).replace('xml', 'json').replace('/5/', '/1000/')
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


def get_puuid(nickname, tag):
    url = f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{nickname}/{tag}?api_key={api_key}'
    res = requests.get(url).json()
    puuid = res['puuid']
    return puuid


def get_match_id(puuid,num):
    url = f'https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={num}&api_key={api_key}'
    match_list = requests.get(url).json()
    return match_list


def get_matches_timelines(matchid):
    url1 = f'https://asia.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={api_key}'
    url2 = f'https://asia.api.riotgames.com/lol/match/v5/matches/{matchid}/timeline?api_key={api_key}'
    matches = requests.get(url1).json()
    timelines = requests.get(url2).json()
    return matches, timelines

def get_rawdata(tier):
    division_list = ['I','II','III','IV']
    lst = []
    page = random.randrange(1,20)
    print('get summonerId....')
    
    for division in tqdm(division_list):
        url = f'https://kr.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{tier}/{division}?page={page}&api_key={api_key}'
        res = requests.get(url).json()
        lst += random.sample(res,3)
    # lst라는 변수에서 summonerId만 리스트에 담기
    summoner_id_list = list(map(lambda x:x['summonerId'] ,lst))
    # summonerId가 담긴 리스트를 통해 puuId
    print('get puuId.....')
    puu_id_list = []
    for summoner_id in tqdm(summoner_id_list):
        url = f'https://kr.api.riotgames.com/lol/summoner/v4/summoners/{summoner_id}?api_key={api_key}'
        res = requests.get(url).json()
        puu_id = res['puuid']
        puu_id_list.append(puu_id)
    
    print('get match_id....')
    match_id_list = []
    #puuId를 통해 matchId를 가져오기 -> 3개씩 담기
    for puu_id in tqdm(puu_id_list):
        match_ids = get_match_id(puu_id,3)
        match_id_list.extend(match_ids)
    print('get matches & timeline....')
    df_create = []
    for match_id in tqdm(match_id_list):
        matches,timelines = get_matches_timelines(match_id)
        df_create.append([match_id,matches,timelines])
    #matches,timeline을 불러서 이중리스트를 만들고 데이터프레임으로 만들어서 - [match_id,matches,timelines]
    df =pd.DataFrame(df_create,columns = ['match_id','matches','timelines'])
    return df
    
    
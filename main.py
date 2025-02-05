# !pip3 install feedparser
# !pip3 install pandas
#-*- coding: utf-8 -*-

import os
from mastodon import Mastodon
from datetime import timedelta, datetime
from dateutil import parser
import requests
import feedparser

access_token = os.getenv('MASTODON_ACCESS_TOKEN')
api_base_url = os.getenv('API_BASE_URL')
zenn_dev_base_url = os.getenv('ZENN_DEV_BASE_URL')

mastodon = Mastodon(
    access_token = access_token,
    api_base_url = api_base_url
)

import requests
import pandas as pd
import random

# 배열을 csv 파일로 저장하는 함수
def export_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# csv 파일을 읽어와서 데이터를 DataFrame으로 반환하는 함수
def read_from_csv(filename):
    try:
        df = pd.read_csv(filename)
        # 데이터프레임이 비어있는지 확인
        if df.empty:
            return []  
    except FileNotFoundError:
        return []
    except pd.errors.EmptyDataError:
        return [] 
    return df

def feed_crawling():
    FEED_URL = 'https://zenn.dev/feed' 

    rss_feed = feedparser.parse(FEED_URL)
    used_items = read_from_csv("used_items.csv")

    data = [] # 데이터 후보_중복이면 체크 안 함

    for entry in rss_feed.entries:
        object = {"title":entry.title, "link": entry.links[0].href}

        if (object in used_items):
          continue
        else:
          data.append(object)


    # 무작위로 하나 선택
    
    if (data == []):
        return # 모두 중복이면 포스팅할 것 없음
    
    print_entry = random.choice(data)

    message = f"""Trend Post\nTitle : {print_entry["title"]}\nLink : {print_entry["link"]}"""
    mastodon.toot(message)

    used_items.append({"title":print_entry["title"], "link":{print_entry["link"]}})

    export_to_csv(used_items, "used_items.csv")

export_to_csv([], "used_items.csv")
feed_crawling()
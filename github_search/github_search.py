# coding: utf-8
import time
import json
import requests
from db import REDIS

from IPython import embed
per_page = 30


SEARCH_API = 'https://api.github.com/search/repositories?q={} stars:>=100&sort=updated&order=desc&per_page={}&page={}'


def search_github(keyword):
    page_cap = 1000 // 30
    res = requests.get(SEARCH_API.format(keyword, 1,0)).json()
    total_count = res['total_count']
    if REDIS.hsetnx('total_count', keyword, total_count ):
        print("{} has {}".format(keyword, total_count))
    total_page = total_count // per_page
    counter = 0
    
    if total_page >= page_cap:
        total_page = page_cap
    for i in range(0, total_page):
        res = requests.get(SEARCH_API.format(keyword, per_page,i)).json()
        if('items' not in res):
            embed()
        repo_list = res['items']
        for repo in repo_list:
            repo_name = repo['html_url']
            desc = {
                'repo_desc': repo['description'],
                'star': repo['stargazers_count'],
                'language': repo['language']
            }
            if REDIS.hsetnx('repos', repo_name, json.dumps(desc)):
                print("{}/{}:{}".format(counter, total_count ,repo_name))
                counter += 1
        time.sleep(10)


if __name__ == '__main__':
    keywords = ["firmware","MCU","microcontroller","STM32","Arduino","FreeRTOS","ESP32","atmel","LPC"]
    for keyword in keywords:
        search_github(keyword)

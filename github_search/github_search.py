# coding: utf-8
import time
import json
import requests
from db import REDIS
from math import ceil

from IPython import embed
per_page = 30


SEARCH_API = 'https://api.github.com/search/repositories?q={} stars:{}&sort=stars&order=desc&per_page={}&page={}'


def search_github(star_cond,keyword):
    res = requests.get(SEARCH_API.format(keyword, star_cond, 1,0)).json()
    total_count = res['total_count']
    #if REDIS.hsetnx('total_count', keyword, total_count ):
    #    print("{} has {}".format(keyword, total_count))
    print("{} under {} has {}".format(keyword, star_cond, total_count))
    total_page = ceil(total_count / per_page)
    counter = 0
    
    for i in range(1, total_page + 1):
        res = requests.get(SEARCH_API.format(keyword, star_cond, per_page,i)).json()
        repo_list = res['items']
        for repo in repo_list:
            repo_name = repo['html_url']
            desc = {
                'repo_desc': repo['description'],
                'star': repo['stargazers_count'],
                'language': repo['language']
            }
            if REDIS.hsetnx('repos', repo_name, json.dumps(desc)):
                print("{}, {}/{}:{}".format(star_cond,counter, total_count ,repo_name))
                counter += 1
        time.sleep(10)

def without_db(keyword):
    page_cap = 1000 // 30
    res = requests.get(SEARCH_API.format(keyword, 1,0)).json()
    total_count = res['total_count']
    total_page = total_count // per_page
    counter = 0
    
    if total_page >= page_cap:
        total_page = page_cap
    for i in range(0, total_page + 1):
        res = requests.get(SEARCH_API.format(keyword, per_page,i)).json()
        if('items' not in res):
            embed()
        repo_list = res['items']
        for repo in repo_list:
            repo_name = repo['html_url']
            with open("stm32.txt","a") as wfile:
                wfile.write("{}/{}:{}\n".format(counter, total_count ,repo_name))
            counter += 1
            print("{}/{}".format(counter,total_count))
        time.sleep(10)

if __name__ == '__main__':
    keywords = ["firmware","MCU","microcontroller","STM32","Arduino","FreeRTOS","ESP32","atmel","LPC"]
    for keyword in keywords:
        star_cond = ">=150"
        search_github(star_cond,keyword)
        star_cond = "100..150"
        search_github(star_cond,keyword)

# encoding: utf-8
from logging import Logger

import requests
from src.util import logger
import configparser
import os
import re
import frozen

log: Logger = logger.get_logger("qq_video")
frozen_path = frozen.get_frozen_path()
cf = configparser.RawConfigParser()
filename = os.path.join(frozen_path, "config", "config.ini")
cf.read(filename, encoding="utf-8")
cf.options("config")
player = cf.get("config", "player_001")


class Episode:
    def __init__(self, no, link):
        self.no = no
        self.link = link


def get_series(url):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               # 'Host': 'v.qq.com',
               # 'Referer': 'https://v.qq.com/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"
               }
    source_id_groups = re.search(r"(\w+?)(?=\.html)", url)
    if not source_id_groups:
        return None
    source_id = source_id_groups[0]
    series_url = "https://s.video.qq.com/get_playsource?id={}&otype=json&range=1-10000&type=4".format(source_id)
    res = requests.get(url=series_url, headers=headers, verify=False)
    series: list[Episode] = []
    if not res.ok:
        log.info("视频请求失败，请求URl【%s】", url)
        return None
    series_group = re.findall(r'"episode_number":"(\d+)",[\s\S]+?"playUrl":"([\s\S]+?)"', res.text)
    if not series_group:
        return None
    for item in series_group:
        no = item[0]
        link = item[1]
        # 转换播放源
        link = player + link
        episode = Episode(no, link)
        series.append(episode)

    # 单页面解析，有明显缺陷
    ''' 
    items = soup.find_all('div', attrs={'class': 'wrapper_main'})[0].find_all("span", attrs={"class": "item"})
    if not items:
        log.info("视频请求失败，请求URl【%s】", url)
        return
    for item in items:
        # 获取链接
        link_soup = item.find_all("a")
        if not link_soup:
            log.info("视频请求失败，请求URl【%s】", url)
            return None
        link = link_soup[0].attrs['href']
        # 转换播放源
        link = player + link

        # 获取集数
        no_soup = link_soup[0].find_all("span")
        if not no_soup:
            log.info("视频请求失败，请求URl【%s】", url)
            return None
        no = no_soup[0].text
        episode = Episode(no, link)
        series.append(episode)
    '''

    return series

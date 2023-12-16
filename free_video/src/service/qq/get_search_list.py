# encoding: utf-8

from bs4 import BeautifulSoup
import requests
from src.util import logger
import configparser
import os
import re
import frozen

log = logger.get_logger("qq_video")
frozen_path = frozen.get_frozen_path()
cf = configparser.RawConfigParser()
filename = os.path.join(frozen_path, "config", "config.ini")
cf.read(filename, encoding="utf-8")
cf.options("config")
player_001 = cf.get("config", "player_001")
detail_url = "/detail?url="


class Video:
    def __init__(self, picture, alt, title, link, labels, desc):
        self.picture = picture
        self.alt = alt
        self.title = title
        self.link = link
        self.labels = labels
        self.desc = desc


def get_list(keywords):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9',
               'Connection': 'keep-alive',
               'Host': 'v.qq.com',
               'Referer': 'https://v.qq.com/',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"
               }
    url = "https://v.qq.com/x/search/?q={}".format(keywords)
    res = requests.get(url=url, headers=headers, verify=False)
    if not res.ok:
        log.info("视频请求失败，请求URl【%s】", url)
        return None
    soup = BeautifulSoup(res.text, 'html5lib')
    items = soup.find_all('div', attrs={'class': 'result_item'})
    if (not items) or len(items) < 1:
        log.info("视频请求失败，请求URl【%s】", url)
        return
    videos = []
    for item in items:
        # 获取封面图片
        figure_soup = item.find_all("img", attrs={"class": "figure_pic"})
        if not figure_soup:
            log.info("页面解析失败，请求URL【%s】", url)
            continue
        src = figure_soup[0].attrs['src']
        alt = figure_soup[0].attrs['alt']
        # 判断是否为系列视频，若是系列视频，则跳转到详情页面
        caption_soup = item.find_all("div", attrs={"class": "_playlist"})
        if caption_soup:
            player = detail_url
        else:
            player = player_001
        # 获取标题
        title_soup = item.find_all("h2", attrs={"class": "result_title"})
        if not title_soup:
            log.info("页面解析失败，请求URL【%s】", url)
            continue
        title = str(title_soup[0])
        # 转换播放源
        title = re.sub(r"href=\"([\S\s]+?)\"", r'href="'+player+r'\1"', title)

        # 获取链接
        link_soup = title_soup[0].find_all("a")
        if not link_soup:
            log.info("页面解析失败，请求URL【%s】", url)
            continue
        link = link_soup[0].attrs['href']
        # 转换播放源
        link = player+link

        # 获取标签
        label_soup = item.find_all("div", attrs={"class": "result_info"})
        if not label_soup:
            log.info("页面解析失败，请求URL【%s】", url)
            continue
        label_item_soup = label_soup[0].find_all("div", attrs={"class": "info_item"})
        if not label_item_soup:
            log.info("页面解析失败，请求URL【%s】", url)
            continue
        labels = []
        for label_item in label_item_soup:
            if "info_item_desc" in label_item.attrs["class"]:
                continue
            label = {}
            label_title = label_item.find_all("span", attrs={"class": "label"})[0].text
            label_content = label_item.find_all("span", attrs={"class": "content"})[0].text
            label["label_title"] = label_title
            label["label_content"] = label_content
            labels.append(label)

        # 获取简介
        desc_soup = label_soup[0].find_all("div", attrs={"class": "info_item info_item_desc"})
        desc = ""
        if desc_soup:
            desc = desc_soup[0].find_all("span", attrs={"class": "desc_text"})[0].text
        video = Video(src, alt, title, link, labels, desc)
        videos.append(video)
    return videos

# -*- coding: utf-8 -*-
import urllib.parse
import json
import codecs

import scrapy

'''
获取 Anidb ID

先取出bangID和name_jp装入全局的map中
用name_jp组装start_urls
得到的结果通过name_jp取出bangID  存储下来
存储的内容有
    anime_bang_id  name_jp  anime_anidb_id
存储目录  ../res_data/anime_bang_anidb_mapping/
'''


class AnidbIDSpider(scrapy.Spider):
    name = "anidbid"
    global start_url_prefix
    start_url_prefix = "http://anidb.net/perl-bin/animedb.pl?adb.search="
    global start_url_suffix
    start_url_suffix = "&show=search&do.search=search"
    global anidb_bang
    anidb_bang = dict()
    anidb_bang['進撃の巨人 Season 2 进击的巨人 第二季'] = '118335'
    start_urls = []
    for ai in anidb_bang:
        url = str(start_url_prefix + ai.replace(" ", "+") + start_url_suffix)
        start_urls.append(url)

    def parse(self, res):
        n_jp = urllib.parse.unquote(
            str(res.url).replace(start_url_prefix, "").replace(start_url_suffix, "").replace("+", " "))
        anime_anidb_id = (res.css('table.search_results').css('td.relid a::attr(href)').extract_first()).split("=")[-1]
        a_map = dict()
        a_map['anime_anidb_id'] = anime_anidb_id
        a_map['name_jp'] = n_jp
        a_map['anime_bang_id'] = anidb_bang[n_jp]
        codecs.open("../res_data/anime_bang_anidb_mapping/" + anidb_bang[n_jp] + ".json", "w", "utf-8").write(
            json.dumps(a_map, ensure_ascii=False))
        print(a_map)

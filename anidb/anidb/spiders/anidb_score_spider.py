# -*- coding: utf-8 -*-
import os
import urllib.parse
import json
import codecs

import scrapy

'''
通过 AnidbID 获取 Anidb Score

前提条件
bangID和AnidbID已经建立好了对应关系
拥有AnidbID列表

存储的内容有
    anime_anidb_id  anime_anidb_rating_weighted  anime_anidb_avg_value
存储目录  ../res_data/anime_anidb_rating/
'''


class AnidbScoreSpider(scrapy.Spider):
    name = "anrating"
    start_url_prefix = "http://anidb.net/perl-bin/animedb.pl?show=anime&aid="
    dir_path = '../res_data/anime_bang_anidb_mapping/'
    anidb_id_list = ['12233', '10750']
    for a_name in os.listdir(dir_path):
        json_item = json.load(open(dir_path + a_name, 'r'))
        if json_item['anime_anidb_id'] is not None:
            anidb_id_list.append(json_item['anime_anidb_id'])
    start_urls = [
        # 'file://H/fisher_p/crawl-anime/web_source/AniDB10750.html',
        # 'file://H/fisher_p/crawl-anime/web_source/AniDB12233.html',
    ]
    for ai in anidb_id_list:
        url = str(start_url_prefix + ai)
        start_urls.append(url)

    def parse(self, res):
        anidb_id = res.url.split("=")[-1]
        a_rating = dict()
        a_rating['anime_anidb_id'] = anidb_id
        for r_css in res.css('div.g_definitionlist span.value'):
            if r_css.css('span::attr(itemprop)').extract_first() == 'ratingValue':
                a_rating['anime_anidb_rating_weighted'] = r_css.css('span::text').extract_first()
            else:
                a_rating['anime_anidb_avg_value'] = r_css.css('span::text').extract_first()
                break
        codecs.open("../res_data/anime_anidb_rating/" + anidb_id + ".json", "w", "utf-8").write(
            json.dumps(a_rating, ensure_ascii=False))
        print(a_rating)

import os

import scrapy
import json

'''
获取 bang ID  存储成json文件
'''


class BangIDSpider(scrapy.Spider):
    name = "bid"
    bang_url_prefix = 'http://bangumi.tv/anime/browser/tv/airtime/2017-1?page='
    start_urls = [
        # 'file:///home/rust/ws/crawl-anime/web_source/s2017-01_p1.html',
    ]
    for i in range(1, 4):
        start_urls.append(bang_url_prefix + str(i))

    def parse(self, res):
        res_list = []
        for l in res.css('h3 a.l'):
            res_list.append(l.css('a::attr(href)').extract_first().split("/")[-1])

        json_dir = "../res_data/anime_bang_id/"
        if not os.path.exists(json_dir):
            print("json dir not found...")
            os.makedirs(json_dir)
            print("Create dir:  " + json_dir)

        json_file = open(json_dir + res.url.split("/")[-1] + '.json', 'w', encoding='utf8')
        json_file.write(json.dumps(res_list, ensure_ascii=False))
        json_file.close()
        print("done with " + res.url)

import os

import scrapy
import json

from bang.items import AnimeBangCoverPicItem  # PyCharm post an error here and I don't know why

'''
下载图片
'''


class CoverPicSpider(scrapy.Spider):
    name = "bpic"
    start_urls = []
    for dir in os.listdir('../res_data/anime_json'):
        if '2017-07' not in dir:
            continue
        for anime_json in os.listdir('../res_data/anime_json/' + dir):
            pic_link = json.load(open('../res_data/anime_json/' + dir + "/" + anime_json, 'r'))['pic_link']
            if pic_link is not None:
                start_urls.append('http:' + pic_link)

    def parse(self, res):
        bang_id = res.url.split("/")[-1].split("_")[0]
        item = AnimeBangCoverPicItem()
        item['file_name'] = "p_" + bang_id + ".jpg"
        item['image_urls'] = [res.url]  # Must be a list
        yield item

        pic_dir = "../res_data/anime_pic/2017-07"
        if not os.path.exists(pic_dir):
            print("json dir not found...")
            os.makedirs(pic_dir)
            print("Create dir:  " + pic_dir)

        print("done download: " + bang_id)

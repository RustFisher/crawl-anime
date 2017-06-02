import os

import scrapy
import json

'''
获取动画的信息  存储成json文件
'''


class AnimeSpider(scrapy.Spider):
    name = "bang"

    start_urls = [
        # 'file:///home/rust/ws/crawl-anime/web_source/a118335.html',
        # 'file:///home/rust/ws/crawl-anime/web_source/a210811.html',
        # 'file:///home/rust/ws/crawl-anime/web_source/a146732.html',
        # 'file://H/fisher_p/crawl-anime/web_source/a118335.html',
    ]

    #  读取JSON中的bang_id
    id_jsons = os.listdir('../res_data/anime_bang_id')
    for json_file in os.listdir('../res_data/anime_bang_id'):
        for single_id in json.load(open('../res_data/anime_bang_id/' + json_file, 'r')):
            start_urls.append('http://bangumi.tv/subject/' + single_id)

    def parse(self, response):
        res = response

        # 获取h1作为title  抓取基本信息
        title = res.css('h1.nameSingle')
        name_jp = title.css('a::text').extract_first()
        a_link = title.css('a::attr(href)').extract_first()
        anime_bang_id = str(a_link).split('/')[-1]
        name_zh = title.css('a::attr(title)').extract_first()
        sub_title = title.css('small::text').extract_first()
        # print(name_jp + " , " + name_zh + " , " + anime_bang_id + " , " + sub_title)

        summary = ""  # 获取简介
        for s in res.css('div.subject_summary::text').extract():
            summary += s

        info = res.css('div.infobox')  # 获取左侧信息表
        pic_link = info.css('a::attr(href)').extract_first()  # 获取封面图片地址

        info_list = []  # 存储左侧信息
        for li in info.css('li'):
            info_title = li.css('span.tip::text').extract_first()
            info_content_href = li.css('a').extract_first()
            list_entity = []
            staff_list = []
            if info_content_href is None:
                staff_list.append(li.css('li::text').extract_first())
            else:
                # 若是链接而且可能有多个链接  将其中的信息提取拼接
                for p in li.css('a'):
                    p_id = p.xpath('@href').extract_first().split("/")[-1]
                    p_name = p.css('a::text').extract_first()
                    staff_list.append(p_name + "%%" + p_id)

            list_entity.append(info_title)
            list_entity.append(staff_list)
            info_list.append(list_entity)

        chars = res.css('div.userContainer')  # get characters and CV
        character_pair_list = []
        for char in chars:
            character_bang_id = char.css('a::attr(href)').extract_first().split("/")[-1]
            character_name = char.css('a::attr(title)').extract_first()
            cv_bang_id = char.css('a::attr(href)')[-1].extract().split("/")[-1]
            cv_name = char.css('a::text')[-1].extract()
            character_pair_list.append(character_name + "%%" + character_bang_id + "%&" + cv_name + "%%" + cv_bang_id)

        print("crawl <<" + name_zh + ">> finish, now save to json " + anime_bang_id)
        anime_dict = dict()  # animation json dictionary
        anime_dict['anime_bang_id'] = anime_bang_id
        anime_dict['sub_title'] = sub_title
        anime_dict['name_jp'] = name_jp
        anime_dict['name_zh'] = name_zh
        anime_dict['pic_link'] = pic_link
        anime_dict['summary'] = summary
        anime_dict['info_list'] = info_list
        anime_dict['character_pair_list'] = character_pair_list

        json_dir = "../res_data/anime_json/2017-01/"  # todo 根据实际情况而改变
        if not os.path.exists(json_dir):
            print("json dir not found")
            os.makedirs(json_dir)
            print("Create dir  " + json_dir)

        json_file = open(json_dir + anime_bang_id + '.json', 'w', encoding='utf8')
        json_file.write(json.dumps(anime_dict, ensure_ascii=False))
        json_file.close()

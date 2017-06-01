import os

import scrapy
import json

'''
获取 people 信息  存储成json文件
'''


class PeopleSpider(scrapy.Spider):
    name = "bp"
    bang_url_prefix = 'http://bangumi.tv/people/'
    start_urls = [
        # 'file:///home/rust/ws/crawl-anime/web_source/p2822.html',

        
        'file://H/fisher_p/crawl-anime/web_source/p1656.html',
        'file://H/fisher_p/crawl-anime/web_source/p2822.html',
        'file://H/fisher_p/crawl-anime/web_source/p7360.html',
        'file://H/fisher_p/crawl-anime/web_source/p9096.html',
        'file://H/fisher_p/crawl-anime/web_source/p13233.html',
    ]
    people_id_list = []

    # for a_id in people_id_list:
    #     start_urls.append(bang_url_prefix + a_id)

    def parse(self, res):
        name = res.css('h1.nameSingle').css('a::text').extract_first()
        pb_id = res.css('h1.nameSingle').css('a::attr(href)').extract_first().split("/")[-1]

        left_info_list = []  # 左侧信息
        left_info = res.css('div.infobox')  # 获取左侧信息表

        for li in left_info.css('li'):
            info_title = li.css('span.tip::text').extract_first()
            info_content_href = li.css('a').extract_first()  # 先判断是不是链接
            list_entity = []
            left_info_content = ""
            if info_content_href is None:
                left_info_content = (li.css('li::text').extract_first())

            list_entity.append(info_title)
            list_entity.append(left_info_content)
            left_info_list.append(list_entity)

        job = "job"  # 职业
        p_detail = ""  # 简介
        productions = []  # 作品
        for cb in res.css('div.column'):
            if cb.css('div::attr(id)').extract_first() == 'columnCrtB':  # 获取中间的 columnCrtB 信息
                for d in cb.css('div.detail::text').extract():
                    p_detail += d
                job = str.strip((cb.css('div.clearit h2::text').extract_first()).split(":")[-1])
                # 根据工作类别进行下一步的抓取
                if "声优" in job:

                    pass
                elif "制作人员" in job:  # 确定这里列出来的都是作品
                    for pr in cb.css('li'):
                        involve_p = dict()
                        involve_p['anime_name'] = pr.css('a::attr(title)').extract_first()
                        involve_p['anime_bang_id'] = pr.css('a::attr(href)').extract_first().split("/")[-1]
                        involve_p['position'] = pr.css('span.badge_job::text').extract()
                        productions.append(involve_p)

        person_obj = dict()
        person_obj['name'] = name
        person_obj['people_bang_id'] = pb_id
        person_obj['job'] = job
        person_obj['base_info'] = left_info_list
        person_obj['productions'] = productions

        json_dir = "../people_json/"
        if not os.path.exists(json_dir):
            print("json dir not found")
            os.makedirs(json_dir)
            print("Create dir  " + json_dir)

        json_file = open(json_dir + pb_id + '.json', 'w', encoding='utf8')
        json_file.write(json.dumps(person_obj, ensure_ascii=False))
        json_file.close()
        print("done with " + pb_id)

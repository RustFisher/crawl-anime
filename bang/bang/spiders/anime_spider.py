import scrapy

''' 获取动画的信息 '''


class AnimeSpider(scrapy.Spider):
    name = "bang"

    start_urls = [
        'file:///home/rust/ws/crawl-anime/web_source/a118335.html',
        'file:///home/rust/ws/crawl-anime/web_source/a210811.html',
        'file:///home/rust/ws/crawl-anime/web_source/a146732.html',
        # 'file://H/fisher_p/crawl-anime/web_source/a118335.html',
    ]

    def parse(self, response):
        res = response

        # 获取h1作为title  抓取基本信息
        title = res.css('h1.nameSingle')
        name_jp = title.css('a::text').extract_first()
        a_link = title.css('a::attr(href)').extract_first()
        anime_bang_id = str(a_link).split('/')[-1]
        name_zh = title.css('a::attr(title)').extract_first()
        sub_title = title.css('small::text').extract_first()
        print(name_jp + " , " + name_zh + " , " + anime_bang_id + " , " + sub_title)

        summary = ""  # 获取简介
        for s in res.css('div.subject_summary::text').extract():
            summary += s
        print(summary)

        info = res.css('div.infobox')  # 获取左侧信息表

        pic_link = info.css('a::attr(href)').extract_first()  # 获取封面图片地址
        print("pic link: " + pic_link)

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

        for le in info_list:
            print(le)

        chars = res.css('div.userContainer')  # get characters and CV
        char_list = []
        for char in chars:
            character_bang_id = char.css('a::attr(href)').extract_first().split("/")[-1]
            character_name = char.css('a::attr(title)').extract_first()
            cv_bang_id = char.css('a::attr(href)')[-1].extract().split("/")[-1]
            cv_name = char.css('a::text')[-1].extract()
            char_list.append(character_name + "%%" + character_bang_id + "%&" + cv_name + "%%" + cv_bang_id)

        print(char_list)

        print("Finish\n")

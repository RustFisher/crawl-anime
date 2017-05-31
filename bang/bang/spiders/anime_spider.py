import scrapy


class AnimeSpider(scrapy.Spider):
    name = "bang"

    start_urls = [
        'file://H/fisher_p/crawl-anime/web_source/a118335.html',
    ]

    def parse(self, response):
        res = response

        # 获取h1作为title  抓取基本信息
        title = res.css('h1.nameSingle')
        name_jp = title.css('a::text').extract_first()
        a_link = title.css('a::attr(href)').extract_first()
        bang_id = str(a_link).split('/')[-1]
        name_zh = title.css('a::attr(title)').extract_first()
        sub_title = title.css('small::text').extract_first()
        print(name_jp + " , " + name_zh + " , " + bang_id + " , " + sub_title)

        # 获取信息表
        info = res.css('div.infobox')

        pic_link = info.css('a::attr(href)').extract_first()  # 获取封面图片地址
        print("pic link: " + pic_link)
        for li in info.css('li'):
            info_title = li.css('span.tip::text').extract_first()
            info_content_href = li.css('a').extract_first()
            if info_content_href is None:
                info_contents = li.css('li::text').extract_first()
            else:
                # 若是链接  将其中的信息提取拼接成一个字符串
                people_bang_id = str(li.css('a::attr(href)').extract_first()).split("/")[-1]
                info_contents = li.css('a::text').extract_first() + "|" + people_bang_id
            print(info_title + " " + str(info_contents))

        print("Finish")

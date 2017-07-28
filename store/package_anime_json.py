# -*- coding: utf-8 -*-

import codecs
import json
import os

import sys

from store import db_config


class PackageJson(object):
    """ 整理json文件给app使用
    """

    @staticmethod
    def output_data():
        """
        从数据库中读出所有的动画数据  存成json
        这里处理后的json文件  直接给APP使用
        :return: None
        """

        a_list_2017_04 = []  # 4月番列表
        a_list_2017_01 = []
        a_list_2017_07 = []

        conn = db_config.get_db_conn()

        cursor = conn.cursor()
        anime_id_list = []

        basic_table_keys = []  # 主表的列名
        cursor.execute('show columns from anime_basic_info')
        for row in cursor.fetchall():
            if row[0] not in basic_table_keys:
                basic_table_keys.append(row[0])
        basic_table_keys.remove('pic_link')  # 不输出封面图片地址

        staff_table_keys = []  # staff表的列名
        cursor.execute("show columns from anime_staff_info")
        for row in cursor.fetchall():
            staff_table_keys.append(row[0])
        staff_table_keys.remove('anime_bang_id')

        cursor.execute('select * from anime_basic_info')
        for r in cursor.fetchall():
            anime_id_list.append(r[0])
        count_anime = len(anime_id_list)
        current = 0
        for anime_id in anime_id_list:
            anime_item = dict()
            anime_staff_info = dict()
            anime_item['anime_bang_id'] = anime_id
            for mk in basic_table_keys:  # 装载基本信息
                #  select 列名称 from 表名称 where 条件;
                cursor.execute('select ' + mk + ' from anime_basic_info where anime_bang_id = ' + anime_id)
                if cursor.rowcount > 0:
                    for r in cursor.fetchall():
                        anime_item[mk] = r[0]
            for sk in staff_table_keys:
                if sk in basic_table_keys:
                    continue
                cursor.execute('select ' + sk + ' from anime_staff_info where anime_bang_id = ' + anime_id)
                if cursor.rowcount > 0:
                    for r in cursor.fetchall():
                        if r[0] is not None:
                            if 'copyrigh' in str(sk).lower():
                                anime_item['copyright'] = r[0]
                            elif 'subject_summary' in str(sk):
                                anime_item['subject_summary'] = r[0]
                            elif sk == 'week':
                                anime_item['week'] = r[0]
                            elif sk == 'cast':
                                continue
                            else:
                                anime_staff_info[sk] = r[0]
            anime_item['anime_staff_info'] = anime_staff_info
            current += 1

            cursor.execute('select cast from anime_cast where anime_bang_id = ' + anime_id)
            if cursor.rowcount > 0:
                for r in cursor.fetchall():
                    if r[0] is not None:
                        anime_item['cast'] = r[0]

            c_season_id = anime_item['season_id']
            if c_season_id == "2017-04":
                a_list_2017_04.append(anime_item)
            elif c_season_id == "2017-01":
                a_list_2017_01.append(anime_item)
            elif c_season_id == "2017-07":
                a_list_2017_07.append(anime_item)

            print("Get --> " + str(current) + "/" + str(count_anime))
            print(anime_item)

        conn.close()

        # 在class里 需要获取到文件的绝对位置sys.path[0] 然后去找存放的地点
        codecs.open(os.path.join(sys.path[0], "output/", "app_data", "2017-04.json"), "w", "utf-8").write(
            json.dumps(a_list_2017_04, ensure_ascii=False))
        codecs.open(os.path.join(sys.path[0], "output", "app_data", "2017-01.json"), "w", "utf-8").write(
            json.dumps(a_list_2017_01, ensure_ascii=False))
        codecs.open(os.path.join(sys.path[0], "output", "app_data", "2017-07.json"), "w", "utf-8").write(
            json.dumps(a_list_2017_07, ensure_ascii=False))


if __name__ == "__main__":
    PackageJson.output_data()

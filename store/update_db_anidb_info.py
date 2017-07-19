# -*- coding: utf-8 -*-

"""
更新数据库中的anidb相关信息
"""
import json
import os

from store import db_config


def create_anime_db():
    """ 建立动画数据库
    前提条件 - 列名配置文件正确
    """
    # 查看mapping文件中有多少个key
    mapping_keys = json.load(open("output/key_mapping_db.json", "r"))
    db_keys = []  # json中所有的key
    basic_info_keys = ['anime_bang_id', 'name_zh', 'name_jp', 'sub_title', 'pic_link']  # 基础信息key

    for k in mapping_keys.values():
        if str(k).lower() not in db_keys:
            db_keys.append(str(k).lower())

    for k in db_keys:
        if " " in k:
            print(k)

    conn = db_config.get_db_conn()

    cursor = conn.cursor()

    # 1. 创建动画基本信息表
    # 基本信息有
    #       anime_bang_id, name_zh, name_jp, sub_title, pic_link
    # table_main = "anime_basic_info"
    # cursor.execute(
    #     "create table " + table_main +
    #     "(anime_bang_id text ,name_zh text,name_jp text,sub_title text,pic_link text)CHARSET=utf8")

    # 2. 创建staff和其他信息表
    # table_anime_staff = "anime_staff_info"
    # sk_count = (len(db_keys) - len(basic_info_keys))
    # current_sk_index = 0
    # for sk in db_keys:
    #     if sk not in basic_info_keys:
    #         add_co_sql = "alter table " + table_anime_staff + " add " + sk + " text"
    #         print(add_co_sql)
    #         cursor.execute(add_co_sql)
    #         current_sk_index += 1
    #         print(str(current_sk_index) + "/" + str(sk_count) + " --> " + sk)

    cursor.close()


def get_anidb_id_list():
    """
    读取 anime_anidb_id
    :return: 装有 anime_anidb_id 与 anime_bang_id 的列表
    """

    anidb_json_dir = '../res_data/anime_bang_anidb_mapping/'
    map_list = []
    for aj_p in os.listdir(anidb_json_dir):
        item = json.load(open(anidb_json_dir + aj_p, 'r'))
        if item['anime_anidb_id'] != 'None' and item['anime_anidb_id'] is not None:
            map_list.append(item)
    return map_list


def update_anidb_id_to_database(map_list):
    """
    更新数据库
    将 anime_anidb_id 与 anime_bang_id 对应起来
    输入2种id对应的 dict list
    """
    conn = db_config.get_db_conn()

    cursor = conn.cursor()
    for item in map_list:
        cursor.execute('select anime_bang_id from anime_basic_info where anime_bang_id = ' + item['anime_bang_id'])
        if cursor.rowcount > 0:
            print(cursor.fetchall()[0][0])
            cursor.execute('update anime_basic_info set anime_anidb_id = \'' + item[
                'anime_anidb_id'] + '\' where anime_bang_id = ' + item['anime_bang_id'])
            conn.commit()
    cursor.close()
    conn.close()


def update_anidb_rating():
    """
    更新数据库种anidb的评分
    前提条件是数据库中已经有相应的列
    读取评分的json  然后更新到库中
    """
    conn = db_config.get_db_conn()

    cursor = conn.cursor()
    rating_dir = '../res_data/anime_anidb_rating/'
    for rf in os.listdir(rating_dir):
        item = json.load(open(rating_dir + rf, 'r'))
        a_id = item['anime_anidb_id']
        if a_id is None or a_id == "None":  # 跳过没有相应id的情况
            continue
        cursor.execute('select anime_anidb_id from anime_basic_info where anime_anidb_id = ' + a_id)
        if cursor.rowcount > 0:
            # 更新数据
            if 'anime_anidb_rating_weighted' in item.keys():
                rating = item['anime_anidb_rating_weighted']
                if rating != 'N/A':
                    cursor.execute(
                        'update anime_basic_info set anime_anidb_rating_weighted = ' + rating
                        + ' where anime_anidb_id = ' + a_id)
                    conn.commit()
            if 'anime_anidb_avg_value' in item.keys():
                avg = item['anime_anidb_avg_value']
                if avg != 'N/A':
                    cursor.execute(
                        'update anime_basic_info set anime_anidb_avg_value = ' + avg
                        + ' where anime_anidb_id = ' + a_id)
                    conn.commit()
            print('Update anidb ' + a_id)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    update_anidb_rating()
# update_anidb_id_to_database(get_anidb_id_list())

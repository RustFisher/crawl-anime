# -*- coding: utf-8 -*-

"""
洗数据

整理job的key  将其与数据库的列名对应起来
读取所有的原始数据json  返回所有的 job key
"""

import codecs
import json
import os
import shutil

import time
from datetime import datetime

from store import db_config

''' 2017-07-19 22:19:45  这个表的英文内容是手动添加的
    key为中文 value为英文的表
    e.g. {"服装设计": "clothing_design", "配音监督": "dubbing_supervisor",}
'''
key_mapping_db_path = 'output/key_mapping_db.json'


def summarize_job_keys():
    """ 统计所有的职位名称 """
    info_keys = []
    dir_path = '../res_data/anime_json/'
    for child_dir in os.listdir(dir_path):
        for jf in os.listdir(dir_path + child_dir):
            for item in (json.load(open(dir_path + child_dir + "/" + jf, 'r')))['info_list']:
                k = str.rstrip(item[0])
                if k.endswith(':'):  # 删掉中文的冒号
                    k = k[:-1]
                if k not in info_keys:
                    info_keys.append(k)

    return sorted(info_keys)


def job_keys_add_to_mapping_json(new_keys):
    """ 将职位名称添加到json文件中
        先检查现有json文件中是否存在这个key  若不存在则新增进去
    """
    key_m = json.load(open(key_mapping_db_path, "r"))
    for k in new_keys:
        if k not in key_m.keys():
            print(k + " not in the record, add now.")
            key_m[k] = ''
    codecs.open(key_mapping_db_path, "w", "utf-8").write(json.dumps(key_m, ensure_ascii=False))


def _backup_mapping_file():
    """ 复制备份文件 """
    shutil.copy(key_mapping_db_path, 'output/backup/key_mapping_db_'
                + time.strftime('%Y-%m-%d_%H%M', time.localtime(time.time())) + '.json')


def _convert_anime_to_db_format():
    """ 洗成可以入库的json格式
    前提条件 - 数据库已经正确地建立 & 已有职位中英文对照资源文件
    读取配置文件
    一个个读取下载得到的json文件 将职位key替换成数据库中对应的列名
    """
    key_dict = json.load(open(key_mapping_db_path, "r"))
    db_keys = []  # json中所有的key

    for k in key_dict.values():
        db_keys.append(k)

    conn = db_config.get_db_conn()

    cursor = conn.cursor()
    basic_table_keys = []  # 主表的列名
    cursor.execute("show columns from anime_basic_info")
    for row in cursor.fetchall():
        basic_table_keys.append(row[0])
    print("basic_table_keys:")
    print(basic_table_keys)

    staff_table_keys = []
    cursor.execute("show columns from anime_staff_info")
    for row in cursor.fetchall():
        staff_table_keys.append(row[0])
    print("staff_table_keys")
    print(staff_table_keys)

    dir_path = '../res_data/anime_json/'
    count = 0
    for sd in os.listdir(dir_path):
        for j_name in os.listdir(dir_path + sd):
            j_item = json.load(open(dir_path + sd + "/" + j_name, 'r'))  # 读取原始数据
            item = dict()  # 整理后的目标数据
            item['season_id'] = sd
            s_summary = str(j_item['summary'])
            s_summary = s_summary.replace("\'", "''")
            s_summary = s_summary.replace("'", "''")
            item['subject_summary'] = s_summary
            for bk in basic_table_keys:  # 取出所有基础信息 basic
                if bk in j_item.keys():
                    item[bk] = j_item[bk]
            for s_info_json in j_item['info_list']:  # 处理职位表
                k = str.rstrip(s_info_json[0])
                if k.endswith(":"):
                    k = k[:-1]
                k = key_dict[k]  # 这里换成了英文的key
                info_value = ""
                if len(s_info_json[1]) == 1:
                    info_value = s_info_json[1][0]
                else:
                    for s_info_item in s_info_json[1]:
                        info_value = info_value + s_info_item + "||"
                item[k] = info_value
            cv_info = ""
            for s_cast in j_item['character_pair_list']:  # 处理声优表
                cv_info = cv_info + s_cast + "||"
            item['cast'] = cv_info
            # 至此 动画信息装载完毕 存成json文件
            codecs.open("output/db_anime_json/" + sd + "/a_" + item["anime_bang_id"] + ".json", "w", "utf-8").write(
                json.dumps(item, ensure_ascii=False))
            count += 1
            print("convert " + str(count) + ", bang_id=" + item["anime_bang_id"])

    conn.close()


def _save_anime_to_db():
    """ 将json数据存入数据库
        前提条件 - json文件已经是符合数据库的格式
    """
    conn = db_config.get_db_conn()

    cursor = conn.cursor()
    basic_table_keys = []  # 主表的列名
    staff_table_keys = []
    cast_table_keys = []
    cursor.execute("show columns from anime_basic_info")
    for row in cursor.fetchall():
        basic_table_keys.append(row[0])

    cursor.execute("show columns from anime_staff_info")
    for row in cursor.fetchall():
        staff_table_keys.append(row[0])

    cursor.execute("show columns from anime_cast")
    for row in cursor.fetchall():
        cast_table_keys.append(row[0])

    print(basic_table_keys)
    print(staff_table_keys)
    print(cast_table_keys)

    dir_path = 'output/db_anime_json/'
    count = 0
    for sd in os.listdir(dir_path):
        for j_name in os.listdir(dir_path + sd):
            print("json load " + j_name)
            j_item = json.load(open(dir_path + sd + "/" + j_name, 'r'))

            # 1. prepare basic_info table
            bang_id = j_item["anime_bang_id"]
            cursor.execute("select * from anime_basic_info where anime_bang_id = " + bang_id)
            if cursor.rowcount == 0:
                # 插入新数据
                cursor.execute(
                    "insert into anime_basic_info (anime_bang_id, season_id) values ('" + bang_id + "', '" + j_item[
                        'season_id'] + "')")
                conn.commit()

            # 2. prepare staff table
            cursor.execute("select * from anime_staff_info where anime_bang_id = " + bang_id)
            if cursor.rowcount == 0:
                cursor.execute(
                    "insert into anime_staff_info (anime_bang_id) values ('" + bang_id + "')")
                conn.commit()

            # 3. prepare cast table
            cursor.execute("select * from anime_cast where anime_bang_id = " + bang_id)
            if cursor.rowcount == 0:
                cursor.execute(
                    "insert into anime_cast (anime_bang_id) values ('" + bang_id + "')")
                conn.commit()

            # 4. prepare anime_description table
            cursor.execute("select * from anime_description where anime_bang_id = " + bang_id)
            if cursor.rowcount == 0:
                cursor.execute(
                    "insert into anime_description (anime_bang_id) values ('" + bang_id + "')")
                conn.commit()

            for k in j_item.keys():
                if k == "anime_bang_id":
                    continue
                # if k == "subject_summary":  # 更新简介
                #     update_sum_sql = "update anime_description set subject_summary = \'" + \
                #                      j_item['subject_summary'] + "\' where anime_bang_id = \"" + bang_id + "\""
                #     print(update_sum_sql)
                #     cursor.execute(update_sum_sql)
                #     conn.commit()
                if k in basic_table_keys:
                    value = j_item[k].replace("'", "''")
                    update_basic_sql = "update anime_basic_info set " + k + " = \'" + \
                                       value + "\' where anime_bang_id = \"" + bang_id + "\""
                    # print(update_basic_sql)
                    # cursor.execute(update_basic_sql)
                    # conn.commit()
                if k in staff_table_keys:
                    value = j_item[k].replace("'", "''")
                    update_staff_sql = "update anime_staff_info set " + k + " = \'" + \
                                       value + "\' where anime_bang_id = \"" + bang_id + "\""
                    # print(update_staff_sql)
                    # cursor.execute(update_staff_sql)
                    # conn.commit()

                if k in cast_table_keys:
                    value = j_item[k].replace("'", "''")
                    update_cast_sql = "update anime_cast set " + k + " = \'" + \
                                      value + "\' where anime_bang_id = \"" + bang_id + "\""
                    # print(update_cast_sql)
                    # cursor.execute(update_cast_sql)
                    # conn.commit()
            count += 1
            print(count)
    cursor.close()


if __name__ == '__main__':
    print(str(datetime.now()) + ' :开始整理职位名称')
    job_keys_add_to_mapping_json(summarize_job_keys())
    print(str(datetime.now()) + ' :整理职位名称完成')
    _convert_anime_to_db_format()
    print(str(datetime.now()) + ' :清洗成数据库格式的json文件')
    _save_anime_to_db()

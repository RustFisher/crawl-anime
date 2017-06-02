# 整理job的key  将其与数据库的列名对应起来
import codecs
import json
import os
import shutil

# 读取所有的原始数据json  返回所有的 job key
import time


def summarize_job_keys():
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


# 先检查现有json文件中是否存在这个key  若不存在则新增进去
def job_keys_add_to_mapping_json(new_keys):
    key_m = json.load(open("output/key_mapping_db.json", "r"))
    for k in new_keys:
        if k not in key_m.keys():
            key_m[k] = ''
    codecs.open("output/key_mapping_db.json", "w", "utf-8").write(json.dumps(key_m, ensure_ascii=False))


# 复制备份文件
def backup_mapping_file():
    shutil.copy('output/key_mapping_db.json', 'output/backup/key_mapping_db_'
                + time.strftime('%Y-%m-%d_%H%M', time.localtime(time.time())) + '.json')

# job_keys_add_to_mapping_json(summarize_job_keys())
# backup_mapping_file()

# -*- coding: utf-8 -*-
import codecs
import json
import os

from store import db_config

calendar_dir = os.path.join("output", "calendar")


def get_calendar_json(season_id):
    print("Start get_calendar_json, season_id=" + season_id)
    conn = db_config.get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        "select anime_bang_id, name_zh, name_jp, update_in_week, update_in_week_str from anime_basic_info "
        "where update_in_week_str is not null and season_id = '" + season_id + "'")
    res_all = cursor.fetchall()
    print("Find data count is %s" % len(res_all))
    res_dict = []
    for i in range(0, len(res_all)):
        res_dict.append(res_all[i])
    print(res_dict)
    cursor.close()
    conn.close()
    json_path = os.path.join(calendar_dir, "calendar_" + season_id + ".json")
    codecs.open(json_path, "w", "utf-8").write(json.dumps(res_dict, ensure_ascii=False))


if __name__ == "__main__":
    print("Start get calendar json")
    get_calendar_json("2018-01")

# -*- coding: utf-8 -*-
from store import db_config


def _get_week_number(week_str_zh):
    if week_str_zh == "星期六":
        return 6
    elif week_str_zh == "星期日":
        return 7
    elif week_str_zh == "星期一":
        return 1
    elif week_str_zh == "星期二":
        return 2
    elif week_str_zh == "星期三":
        return 3
    elif week_str_zh == "星期四":
        return 4
    elif week_str_zh == "星期五":
        return 5


def update_anime_update_in_week():
    print("Start update update_in_week column")
    conn = db_config.get_db_conn()
    cursor = conn.cursor()

    cursor.execute("select anime_bang_id, week, name_zh from anime_staff_info")
    staff_all = cursor.fetchall()
    print(staff_all)
    for s in range(0, len(staff_all)):
        if staff_all[s][1] is None:
            continue
        sql_update_basic_info = "update anime_basic_info set update_in_week_str = '" + \
                                staff_all[s][1] + "', update_in_week = " + \
                                str(_get_week_number(staff_all[s][1])) + \
                                " where anime_bang_id = " + staff_all[s][0]
        print("Executing sql line %d: %s" % (s, sql_update_basic_info))
        cursor.execute(sql_update_basic_info)
        conn.commit()
    cursor.close()
    conn.close()
    print("Update update_in_week column finish")


if __name__ == "__main__":
    print("Start update...")
    update_anime_update_in_week()

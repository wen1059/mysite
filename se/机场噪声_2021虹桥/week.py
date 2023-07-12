import re
import math
import os
import day


def cal_lwecpn_week(lamaxpb, hb):
    res = lamaxpb + 10 * math.log10((hb['day'] + 3 * hb['dust'] + 10 * hb['night']) / 7) - 27
    return round(res, 2)


def cal_week(weekwalkpath):
    """
    核心功能程序，计算,7天合并到一个dict，替换的max是7天中最大的
    :param weekwalkpath: 根目录下的二级目录
    :return:
    """
    hb = {'day': 0, 'dust': 0, 'night': 0}
    dic = {}
    file24name = ''
    for file24name, sht in day.yieldsht(weekwalkpath):
        day.count_hb(sht, hb, )
        day.gendic(sht, dic, )
    dic = day.gendic_addmax(dic)
    lamaxp_all = day.gen_lamaxp_all(dic)
    lamaxpb = day.cal_bar(lamaxp_all)
    lwecpn = cal_lwecpn_week(lamaxpb, hb)
    sumresult = (dw := (lambda x: re.search(r'(\d{1,2})#(\d{2,4})', x).group(1))(file24name),
                 '', hb['day'], hb['dust'], hb['night'], sum(hb.values()), lamaxpb, lwecpn)
    return sumresult


def cal_week2(weekwalkpath):
    """
    核心功能程序，计算，每天一个dict，替换的max是每天最大的
    :param weekwalkpath: 根目录下的二级目录
    :return:
    """
    hb_week = {'day': 0, 'dust': 0, 'night': 0}
    lamaxp_all_week = []
    file24name = ''
    for file24name, sht in day.yieldsht(weekwalkpath):
        day.count_hb(sht, hb_week, )
        dic_day = day.gendic_addmax(day.gendic2(sht))
        lamaxp_all_day = day.gen_lamaxp_all(dic_day)
        lamaxp_all_week.extend(lamaxp_all_day)
    lamaxpb_week = day.cal_bar(lamaxp_all_week)
    lwecpn_week = cal_lwecpn_week(lamaxpb_week, hb_week)
    sumresult_week = (dw := (lambda x: re.search(r'(\d{1,2})#(\d{2,4})', x).group(1))(file24name),
                 '', hb_week['day'], hb_week['dust'], hb_week['night'], sum(hb_week.values()), lamaxpb_week, lwecpn_week)
    return sumresult_week


def run_week(walkpath):
    """
    程序入口，写入mysql
    :param walkpath:总目录,得到的下层目录作为yieldsht的os.walk的根目录
    :return:
    """
    db = day.Mysqldb()
    # db.cleartab('week')
    for weekwalkpath, _, _ in os.walk(walkpath):
        if weekwalkpath == walkpath:
            continue
        sumres = cal_week2(weekwalkpath)
        db.ins_to_tab('week', sumres)


if __name__ == '__main__':
    run_week(r"C:\Users\Administrator\Desktop\噪声桌面\复算")

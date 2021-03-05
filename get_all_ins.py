# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         get_all_ins
# Description:  
# Author:       guohuanyang
# Date:         2021/3/3
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
from test_api import request_by_ins_num
from queue import Queue
task_queue = Queue()


class Institution:
    """
    机构信息
    """
    def __init__(self, name, code, ratio, level=0, parent_ins_num=None, status=False, msg=''):
        self.ins_name = name
        self.ins_num = code
        self.ratio = ratio
        self.level = level
        self.parent_ins_num = parent_ins_num
        self.status = status
        self.msg = msg


def bfs_ins():
    founded_shareholders = list()
    founded_shareholder_ins = list()
    while not task_queue.empty():
        institution = task_queue.get()
        print(institution)
        if not institution.ins_num:
            institution.status = True
            institution.msg = 'ins_num不能为空'
            continue
        if institution.ins_num in founded_shareholder_ins:
            institution.msg = '已在前面的层级发现,加入到搜索结果,但不再搜索股东'
            institution.status = True
            founded_shareholders.append(institution)
            continue

        founded_shareholders.append(institution)
        founded_shareholder_ins.append(institution.ins_num)

        res = request_by_ins_num(institution.ins_num)
        res_data = res.json().get("data", {})
        if res_data.get("total", 0) == 0:
            institution.msg = '搜索不到股东信息'
            institution.status = True
            continue

        data_list = res_data.get("dataList", [])
        for item in data_list:
            shah_name = item.get("shah_name", "")
            shah_num = item.get("shah_num", "")
            hold_ratio = item.get("hold_wght_rati", 0.0)

            sub_shareholder = Institution(
                shah_name, shah_num, hold_ratio,
                institution.level+1, institution.ins_num)
            task_queue.put(sub_shareholder)

        institution.status = True
    return founded_shareholders


if __name__ == '__main__':
    test_code = 'cea37295-334a-43a5-9db8-89731f99b096'
    test_obj = Institution('test', test_code, 999)
    task_queue.put(test_obj)
    shareholder_list = bfs_ins()
    print(shareholder_list)

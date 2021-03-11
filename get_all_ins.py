# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         get_all_ins
# Description:  
# Author:       guohuanyang
# Date:         2021/3/3
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
from fn_api import request_by_ins_num
import json
from queue import Queue


class Institution:
    """
    机构信息
    """
    def __init__(self, ins_name, ins_num, ratio, level=0, parent_ins_num=None, status=False, msg=''):
        self.ins_name = ins_name
        self.ins_num = ins_num
        self.ratio = ratio
        self.level = level
        self.parent_ins_num = parent_ins_num
        self.status = status
        self.msg = msg


def bfs_ins(task_queue):
    founded_shareholders = list()
    founded_shareholder_ins = list()
    while not task_queue.empty():
        institution = task_queue.get()
        print(institution.ins_name)
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


def obj2dict(ins_list):
    return [ins.__dict__ for ins in ins_list]


if __name__ == '__main__':
    test_code = 'cea37295-334a-43a5-9db8-89731f99b096'
    test_task_queue = Queue()
    test_obj = Institution('test', test_code, 100)
    test_task_queue.put(test_obj)
    shareholder_list = bfs_ins(test_task_queue)
    print(len(shareholder_list))
    result = obj2dict(shareholder_list)
    json_result = json.dumps(result)
    with open('result.json', 'w') as f:
        f.write(json_result)
    print(result)

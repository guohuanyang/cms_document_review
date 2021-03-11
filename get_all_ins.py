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


def obj2dict(ins_list):
    return [ins.__dict__ for ins in ins_list]


if __name__ == '__main__':
    test_code = 'cea37295-334a-43a5-9db8-89731f99b096'
    # test_task_queue = Queue()
    # test_obj = Institution('test', test_code, 100)
    # test_task_queue.put(test_obj)
    # shareholder_list = bfs_ins(test_task_queue)
    # print(len(shareholder_list))
    # result = obj2dict(shareholder_list)
    # json_result = json.dumps(result)
    # with open('result.json', 'w') as f:
    #     f.write(json_result)
    # print(result)

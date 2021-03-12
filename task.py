# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         task
# Description:  
# Author:       guohuanyang
# Date:         2021/3/11
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
import json
import os
from queue import Queue

import cn2an

from get_all_ins import Institution, obj2dict
from fn_api import request_by_ins_num
from config import json_path
from tree_resource import get_root
from write_excel import WriteExcel
from write_word import main as write_word_template

task_queue = Queue()


class Shareholder_Due_Diligence:
    """
    股东尽调
    """
    def __init__(self, ins_num, ins_name=None, ratio=0, bfs_res='', dfs_res='', header=''):
        self.ins_num = ins_num
        self.ins_name = ins_name or self.set_ins_name()
        self.ratio = "%.2f" % ratio
        self.msg = ''
        self.header = header
        self.level = 0
        self.bfs_res = bfs_res or self.get_bfs_res()
        self.dfs_res = dfs_res or self.bfs2dfs()

    def set_ins_name(self):
        ins_name = ''
        print('未传入机构名称,开始查询机构名称')
        data_list = request_by_ins_num(self.ins_num)
        if len(data_list) == 0:
            self.msg = '搜索不到股东信息'
        if data_list:
            ins_name = data_list[0].get("ins_fn", "")
        print('查询机构名称完成')
        return ins_name

    def get_bfs_res(self):
        ins_obj = Institution(self.ins_name, self.ins_num, self.ratio)
        task_queue.put(ins_obj)
        shareholder_list = bfs_ins()
        bfs_result = obj2dict(shareholder_list)
        if not bfs_result:
            return []
        bfs_json_result = json.dumps(bfs_result)
        bfs_json_path = '%s/%s' % (json_path, 'bfs_result.json')
        if not os.path.exists(json_path):
            os.mkdir(json_path)
        with open(bfs_json_path, 'w', encoding='utf-8') as f:
            f.write(bfs_json_result)
        print('当前搜索的机构名称为{}'.format(self.ins_name))
        return bfs_result

    def bfs2dfs(self):
        print('开始处理股东数据')
        print('搜索到的所有股东记录总数为{}'.format(len(self.bfs_res)))
        if not self.bfs_res:
            return {}
        root = get_root(self.bfs_res)
        print('转为结构化数据')
        return root

    def gen_header(self):
        level_dict = {}
        levels = ['名称']
        for item in self.bfs_res:
            key = item.get('level')
            # 0级即是root，从第一级开始统计
            if key and key not in level_dict:
                level_dict[key] = True
                self.level += 1
                levels.append("第%s层级" % cn2an.an2cn(self.level, "low"))
        print(levels)
        return levels

    def write_data_excel(self):
        print('开始生成excel')
        levels = self.header or self.gen_header()
        excel_obj = WriteExcel(levels)
        excel_obj.write_header()
        print('写表头完成')
        excel_obj.dfs_write(self.dfs_res)
        print('写表格完成')
        excel_obj.save()
        print('保存excel完成')


def bfs_ins():
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

        data_list = request_by_ins_num(institution.ins_num)
        if len(data_list) == 0:
            institution.msg = '搜索不到股东信息'
            institution.status = True
            continue

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


def test_case():
    from tree_resource import read_json
    test_json = read_json('result.json')
    test_ins_num = 'cea37295-334a-43a5-9db8-89731f99b096'
    instance = Shareholder_Due_Diligence(test_ins_num, ins_name='test', bfs_res=test_json)
    instance.write_data_excel()
    write_word_template(instance.dfs_res)


def start_task(ins_num):
    instance = Shareholder_Due_Diligence(ins_num)
    instance.write_data_excel()
    write_word_template(instance.dfs_res)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        query_in_num = sys.argv[1]
        # query_in_num = '408c5e9f-c128-430e-b38b-02c9094b673b'
        start_task(query_in_num)
    else:
        print('缺少输入机构编码')
    # test_case()
    print('任务结束')

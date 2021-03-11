# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         task
# Description:  
# Author:       guohuanyang
# Date:         2021/3/11
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
from get_all_ins import Institution, bfs_ins, obj2dict
from test_api import *


class Shareholder_Due_Diligence:
    """
    股东尽调
    """
    def __init__(self, ins_num):
        self.query_ins_num = ins_num
        self.ins_name = self.set_ins_name()
        self.bfs_res = self.get_bfs_res()
        self.dfs_res = self.bfs2dfs()


    def set_ins_name(self):
        pass

    def get_bfs_res(self):
        ins_obj = Institution(self.ins_name)

    def bfs2dfs(self):
        pass


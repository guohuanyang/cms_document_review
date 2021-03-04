# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         get_all_ins
# Description:  
# Author:       guohuanyang
# Date:         2021/3/3
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
from test_api import request_by_ins_num


class Institution:
    """
    机构信息
    """
    def __init__(self, name, code, ratio):
        self.ins_name = name
        self.ins_num = code
        self.ratio = ratio
        self.shareholder = list()

    def get_shareholder(self):
        if not self.ins_num:
            return
        res = request_by_ins_num(self.ins_num)
        res_data = res.json().get("data", {})
        total_shareholder = res_data.get("total", 0)
        if total_shareholder == 0:
            return
        data_list = res_data.get("dataList", [])
        for item in data_list:
            shah_name = item.get("shah_name", "")
            shah_num = item.get("shah_num", "")
            hold_ratio = item.get("hold_wght_rati", 0.0)
            sub_shareholder = Institution(shah_name, shah_num, hold_ratio)
            sub_shareholder.get_shareholder()
            print(sub_shareholder)
            self.shareholder.append(sub_shareholder)


if __name__ == '__main__':
    test_code = 'cea37295-334a-43a5-9db8-89731f99b096'
    test_obj = Institution('test', test_code, 100)
    test_obj.get_shareholder()
    print(test_obj)

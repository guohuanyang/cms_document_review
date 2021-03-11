# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         test
# Description:  
# Author:       guohuanyang
# Date:         2021/3/10
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
import json
from write_excel import WriteExcel


json_result_path = 'dfs.json'


def read_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f, encoding='utf-8')
        print(json_data)
    return json_data


if __name__ == '__main__':
    root = read_json(json_result_path)
    obj = WriteExcel()
    obj.dfs_write(root)
    # obj.merge_cells()
    obj.save()

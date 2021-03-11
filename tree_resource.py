# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         tree_resource
# Description:  
# Author:       guohuanyang
# Date:         2021/3/5
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
import json

json_result_path = 'result.json'


class Node:
    def __init__(self, obj):
        self.root = obj
        self.children = list()


def read_json(json_path):
    with open(json_path, 'r') as f:
        json_data = json.load(f, encoding='utf-8')
        print(json_data)
    return json_data


def write_json(json_data):
    with open('中文.json', 'w') as f:
        f.write(str(json_data))


def init_root(json_data):
    root = {
        'data': json_data[0],
        'children': list()
    }
    return root


found_ins_num = []


def dfs(root, json_data, level=1):
    root_ins_num = root['data']['ins_num']
    level_data = [x for x in json_data if x['level'] == level and x['parent_ins_num'] == root_ins_num]
    if not level_data:
        return
    for child_data in level_data:
        ins_num = child_data['ins_num']
        if ins_num not in found_ins_num:
            found_ins_num.append(ins_num)
            child = {
                'data': child_data,
                'children': list()
            }
            print(child)
            dfs(child, json_data, level+1)
            root['children'].append(child)


def get_root(json_data):
    root = init_root(json_data)
    dfs(root, json_data, 1)
    return root


def add_cols_num(json_data: list):
    if not json_data:
        return
    for item in json_data:
        item['col_num'] = 0

    result = dict()
    for item in json_data:
        result[item['ins_num']] = 0

    for item in reversed(json_data):
        ins_num = item['ins_num']
        if ins_num in result:
            if result[ins_num] == 0:
                result[ins_num] += 1
            parent_ins_num = item['parent_ins_num']
            if parent_ins_num in result:
                if not item['msg']:
                    result[parent_ins_num] += result[ins_num]
                else:
                    result[parent_ins_num] += 1

    for item in json_data:
        item['col_num'] = result[item['ins_num']]

    return json_data


def gen_dict_data(json_data):
    dict_dat = {}
    for item in json_data:
        if item['level'] not in dict_dat:
            dict_dat[item['level']] = [item]
        else:
            dict_dat[item['level']].append(item)
    return dict_dat


if __name__ == '__main__':
    t = read_json(json_result_path)
    test_root = get_root(t)
    root_str = json.dumps(test_root)
    with open('dfs.json', 'w')as f:
        f.write(root_str)
    print(test_root)

    # res = add_cols_num(t)
    # write_json(t)

# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         write_excel
# Description:
# Author:       guohuanyang
# Date:         2021/3/10
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
import os
from datetime import datetime

import openpyxl

dir_name = 'result'
sheet = []


class WriteExcel:
    """
    按照模版写入excel文件
    """

    def __init__(self, head=None):
        wb = openpyxl.Workbook()
        self.wb = wb
        self.ws = wb.active
        self.line_num = 1
        self.merge_level = 2
        self.header = head or list()

    def write_by_xy(self, data):
        start = 0
        end = data['level'] * self.merge_level
        if end > 1:
            start = end - 1
            self.ws.cell(self.line_num + 1, start + 1, data['ins_name'])
            data['cell_1'] = {
                "row": self.line_num + 1,
                "col": start + 1,
            }
            self.ws.cell(self.line_num + 1, start + 2, "%s%%" % data['ratio'])
            data['cell_2'] = {
                "row": self.line_num + 1,
                "col": start + 2,
            }
            # self.ws.cell(self.line_num + 1, start + 3, data['msg'] or '正常')
        else:
            self.ws.cell(self.line_num + 1, start + 1, data['ins_name'])
            data['cell_1'] = {
                "row": self.line_num + 1,
                "col": start + 1,
            }

    def write_head(self, levels):
        self.ws.append(levels)

    def judge_end_point(self, row_num, col_num):
        length = 0
        for row in self.ws.iter_rows(min_row=row_num, max_row=row_num):
            row_list = [cell.value for cell in row]
            for index, value in enumerate(row_list):
                if value:
                    length = index+1
        return col_num<length

    def merge(self, col, col_num):
        values = [item.value for item in col]
        for i in range(0, len(values)):
            if values[i]:
                merge_num = 0
                for j in range(i+1, len(values)):
                    # 不为空或者为叶子结点
                    #   or self.judge_end_point(j, col_num+1)
                    if values[j]:
                        break
                    else:
                        merge_num += 1
                if merge_num and self.judge_end_point(i+1, col_num+1) and self.judge_end_point(i+1+merge_num, col_num+1):
                    self.ws.merge_cells(start_row=i+1, end_row=i+merge_num+1, start_column=col_num, end_column=col_num)
                    # i += merge_num

    def merge_cells(self):
        col_num = 1
        for col in self.ws.iter_cols():
            self.merge(col, col_num)

            col_num += 1

    def dfs_write(self, root):
        data = root['data']
        self.write_by_xy(data)
        if len(root['children'])==0:
            self.line_num += 1
            # merge_line_num += 1
        for children in root['children']:
            self.dfs_write(children)
        self.merge_children(root)

    def merge_children(self, root):
        children = root['children']
        # 孩子节点数量大于1的
        if len(children) > 1:
            # 该节点的行
            start_row_num = root['data']['cell_1']['row']
            # 最后一个孩子节点的行
            end_row_num = children[-1]['data']['cell_1']['row']
            # 该节点的列
            start_col_num = root['data']['cell_1']['col']
            # 根节点
            if start_col_num == 1:
                self.ws.merge_cells(start_row=start_row_num, end_row=end_row_num, start_column=start_col_num,
                                    end_column=start_col_num)
                root['data']['cell_1'] = {
                    "row": end_row_num,
                    "col": start_col_num,
                }
            else:
                self.ws.merge_cells(start_row=start_row_num, end_row=end_row_num, start_column=start_col_num,
                                    end_column=start_col_num)
                root['data']['cell_1'] = {
                    "row": end_row_num,
                    "col": start_col_num,
                }
                self.ws.merge_cells(start_row=start_row_num, end_row=end_row_num, start_column=start_col_num+1,
                                    end_column=start_col_num+1)
                root['data']['cell_2'] = {
                    "row": end_row_num,
                    "col": start_col_num+1,
                }
        elif len(children) == 1:
            start_row_num = root['data']['cell_1']['row']
            end_row_num = children[0]['data']['cell_1']['row']
            start_col_num = root['data']['cell_1']['col']
            if start_col_num == 1:
                self.ws.merge_cells(start_row=start_row_num, end_row=end_row_num, start_column=start_col_num,
                                    end_column=start_col_num)
                root['data']['cell_1'] = {
                    'row': end_row_num,
                    'col': start_col_num
                }
            else:
                self.ws.merge_cells(start_row=start_row_num, end_row=end_row_num, start_column=start_col_num,
                                    end_column=start_col_num)
                root['data']['cell_1'] = {
                    'row': end_row_num,
                    'col': start_col_num
                }
                self.ws.merge_cells(start_row=start_row_num, end_row=end_row_num, start_column=start_col_num+1,
                                    end_column=start_col_num+1)
                root['data']['cell_2'] = {
                    'row': end_row_num,
                    'col': start_col_num+1
                }

    def save(self, save_dir=dir_name):
        file_name = datetime.now().strftime("%Y%m%d-%H%M%S") + '.xlsx'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        excel_file_path = "%s/%s" % (save_dir, file_name)
        self.wb.save(excel_file_path)

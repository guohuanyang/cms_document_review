# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------------
# Name:         config
# Description:  
# Author:       guohuanyang
# Date:         2021/3/11
# Email         guohuanyang@datagrand.com
# -------------------------------------------------------------------------------
environment = 'test'

dev_config = {
    'test': {
        "host": '172.253.33.12:8080',
        "access_token": 'Basic bGlxaXVqaW46bGlxaXVqaW5AUVdlckAxMjM=',
        "headers": {
            'uap-request-id': '11e7c800-d89c-4064-ab49-503deeb0ee25',
            'uap-server-type': '667',
            'uap-request-no': '1003',
            'uap-licence-key': '405a2487-2bc5-4603-beec-a5379f6c3411',
            'uap-user-no': 'test'
        }
    },
    'product': {
        "host": '172.16.10.2:8080',
        "access_token": 'Basic ZGRkc3VzZXI6QmJzZHlpY2hhbzEyMjQhQCMj',
        "headers": {
            'uap-request-id': '1553ef50-dfd3-11e8-879d-00155d462155',
            'uap-server-type': '667',
            'uap-request-no': '1003',
            'uap-licence-key': '1553ef50-dfd3-11e8-879d-00155d462155',
            'uap-user-no': 'test'
        }
    }
}

global_conf = dev_config[environment]

json_path = './json_result'

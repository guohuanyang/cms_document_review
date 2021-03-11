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
        "access_token": 'Basic ZGRkc3VzZXI6QmJzZHlpY2hhbzEyMjQhQCMj',
        "test_ins_num": "cea37295-334a-43a5-9db8-89731f99b096",
        "headers": {
            'uap-server-type': '667',
            'uap-request-no': '1003',
            'uap-licence-key': '405a2487-2bc5-4603-beec-a5379f6c3411',
            'uap-user-no': 'test'
        }
    },
    'product': {
        "host": '172.253.33.12:8080',
        "access_token": 'Basic ZGRkc3VzZXI6QmJzZHlpY2hhbzEyMjQhQCMj',
        "test_ins_num": "cea37295-334a-43a5-9db8-89731f99b096",
        "headers": {
            'uap-server-type': '667',
            'uap-request-no': '1003',
            'uap-licence-key': '405a2487-2bc5-4603-beec-a5379f6c3411',
            'uap-user-no': 'test'
        }
    }
}

global_conf = dev_config[environment]

json_path = './json_result'

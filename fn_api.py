import requests
from config import global_conf


def request_by_ins_num(ins_num):
    """
    根据ins_num 搜索机构的股东信息
    :param ins_num:
    :return:
    """
    url = "http://{host}/api/bussiness_info/get_ins_shah_new?access_token={access_token}".format(
        host=global_conf['host'],
        access_token=global_conf['access_token']
    )

    payload={
        'insNum': ins_num,
        'pageNum': 1,
        'pageSize': 1000,
        # 'isHis': ''
    }
    files=[]
    headers = global_conf['headers']
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200
    # print(response.json())
    return response

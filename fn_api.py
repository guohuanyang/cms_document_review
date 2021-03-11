import requests
from config import global_conf


def request_by_page(ins_num, page_num=1):
    url = "http://{host}/api/bussiness_info/get_ins_shah_new?access_token={access_token}".format(
        host=global_conf['host'],
        access_token=global_conf['access_token']
    )

    payload = {
        'insNum': ins_num,
        'pageNum': page_num,
        'pageSize': 100,
        # 'isHis': ''
    }
    files = []
    headers = global_conf['headers']
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200
    return response


def request_by_ins_num(ins_num):
    """
    根据ins_num 搜索机构的股东信息
    :param ins_num:
    :return:
    """
    response = request_by_page(ins_num)
    res_data = response.json().get('data', dict())
    total = res_data.get('total', 0)
    data_list = res_data.get('dataList', list())
    page_num = 2
    while total>0 and total>len(data_list):
        tmp_response = request_by_page(ins_num, page_num)
        tmp_res_data = tmp_response.json().get('data', dict())
        tmp_data_list = tmp_res_data.get('dataList', list())
        data_list.extend(tmp_data_list)
        page_num += 1
    return data_list


    # print(response.json())
    return response

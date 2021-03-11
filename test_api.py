import requests
host = '172.253.33.12:8080'
access_token = 'Basic ZGRkc3VzZXI6QmJzZHlpY2hhbzEyMjQhQCMj'
test_ins_num = "cea37295-334a-43a5-9db8-89731f99b096"
headers = {
    'uap-server-type': '667',
    'uap-request-no': '1003',
    'uap-licence-key': '405a2487-2bc5-4603-beec-a5379f6c3411',
    'uap-user-no': 'test'
}


def request_by_ins_num(ins_num=test_ins_num):

    url = "http://{host}/api/bussiness_info/get_ins_shah_new?access_token={access_token}".format(
        host=host,
        access_token=access_token
    )

    payload={
        'insNum': ins_num,
        'pageNum': 1,
        'pageSize': 1000,
        # 'isHis': ''
    }
    files=[]

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    assert response.status_code == 200
    # print(response.json())
    return response

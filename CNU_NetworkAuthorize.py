import requests
import dotenv
import os

dotenv.load_dotenv()

cookies = {
    "username": os.environ["username"],
    "password": os.environ["password"],
}

headers = {
  "Origin": "https://cc.nsu.edu.cn",
  "Referer": "https://cc.nsu.edu.cn",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7",
}

student_id = os.environ["username"]                                       # 这里改成你的学号
account_password = os.environ["password"]              # 这里改成你的密码
data_since_login = {"username":student_id, "password":account_password,"remember":"true","DoWhat":"Login"}
data_since_get_info = {"DoWhat":"GetInfo"}
data_since_open_net = {"DoWhat":"OpenNet","Package":f"学生-{os.environ['ISP']}-100M"}

auth_url = "https://cc.nsu.edu.cn/Auth.ashx"

try:
    response = requests.post(auth_url, headers=headers, json=data_since_login, cookies=cookies, verify=False)
    print(response.json()["Message"])

    if (response.json()["Message"] != "身份验证成功！"):
        exit()

    response = requests.post(auth_url, headers=headers, json=data_since_get_info, cookies=cookies, verify=False)
    print(response.json()["Message"])

    if (response.json()["Message"] != "查询信息成功！"):
        exit()

    ip = response.json()["Data"]["IP"]
    mac = response.json()["Data"]["MAC"]
    student_name = response.json()["Data"]["XM"]

    response = requests.post(auth_url, headers=headers, json=data_since_open_net, cookies=cookies, verify=False)
    print(response.json()["Message"])

    if (response.json()["Message"] != "上线成功!" and response.json()["Message"] != "同时登录数已达上限！"):
        exit()

    print(f"\nOkk啦， {student_name}同学， 尽情冲浪吧！\n当前IP：{ip}\n当前mac：{mac}\n当前学号：{student_id}")
except Exception as e:
    print("发生错误")
    # print(e)
    with open("log", "w", encoding="utf8") as f:
        f.write(e.__str__())
    
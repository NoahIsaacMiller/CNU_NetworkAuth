from u679c import encrypt
import requests
import os
import json

# 禁用代理
proxies = {
    "http": None,
    "https": None
}

def createConfigurationFile():
    data = {
        "username": "这里改成你的学号",
        "password": "这里改成你的校园网密码",
        "ISP": "这里改成你的运营商: [电信|联通|移动]"
    }
    f = open("./userConf.json", "w", encoding="utf8")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.close()


# 如果配置文件不存在, 先创建配置文件
if not os.path.exists("./userConf.json"):
    createConfigurationFile()


try:
    f = open("./userConf.json", "r", encoding="utf8")
    userInfo = json.load(f)
except json.JSONDecodeError:
    print("配置文件格式错误")
finally:
    f.close()


student_id = userInfo["username"]                   
account_password = encrypt(student_id, userInfo["password"])


# 构造cookies
cookies = {
    "username": student_id,
    "password": account_password
}

# 构造headers
headers = {
  "Origin": "http://cc.nsu.edu.cn",
  "Referer": "http://cc.nsu.edu.cn",
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
  "Accept": "application/json, text/plain, */*",
  "Accept-Encoding": "gzip, deflate, br, zstd",
  "Accept-Language": "en-US,en;q=0.9,zh;q=0.8,zh-CN;q=0.7",
}


data_since_login = {"username":student_id, "password": account_password,"remember":"true","DoWhat":"Login"}
data_since_get_info = {"DoWhat":"GetInfo"}
data_since_open_net = {"DoWhat":"OpenNet","Package":f"学生-{os.environ['ISP']}-100M"}

auth_url = "http://cc.nsu.edu.cn/Auth.ashx"

response = requests.post(auth_url, headers=headers, json=data_since_login, cookies=cookies, verify=False, proxies=proxies)
print(response.json()["Message"])

if (response.json()["Message"] != "身份验证成功！"):
    exit()

response = requests.post(auth_url, headers=headers, json=data_since_get_info, cookies=cookies, verify=False, proxies=proxies)
print(response.json()["Message"])

if (response.json()["Message"] != "查询信息成功！"):
    exit()

ip = response.json()["Data"]["IP"]
mac = response.json()["Data"]["MAC"]
student_name = response.json()["Data"]["XM"]

response = requests.post(auth_url, headers=headers, json=data_since_open_net, cookies=cookies, verify=False, proxies=proxies)
print(response.json()["Message"])

if (response.json()["Message"] != "上线成功!" and response.json()["Message"] != "同时登录数已达上限！"):
    exit()

print(f"\nOkk啦， {student_name}同学， 尽情冲浪吧！\n当前IP：{ip}\n当前mac：{mac}\n当前学号：{student_id}")

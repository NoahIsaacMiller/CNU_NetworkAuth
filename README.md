# 成都东软校园网认证
## 依赖库安装
`pip install requests pycryptodome -i https://pypi.tuna.tsinghua.edu.cn/simple`

## 需要配置的地方
`.env`文件保存了你的学号，密码，和运营商名字
你需要修改`.env`文件里的三条记录
> 将.env的内容按如下方式修改

```
username=你的学号
password=你的密码
ISP=你的运营商: [移动|联通|电信]
# 比如
# ISP=电信
```
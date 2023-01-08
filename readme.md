# 文本标注后端

## 使用

1. 安装requirement.txt

2. 运行db.py，初始化数据库

3. 运行app.py，启动后端

会以debug模式运行

## 需要注意的

用户密码是以明文存放在数据库中的。  
因为我测试时经常忘记密码。。  
可以参照[flask教程](https://dormousehole.readthedocs.io/en/latest/tutorial/views.html)将密码加密。  
但我也没有写修改密码的功能。  

而且默认第一位注册的用户是管理员。  
其余全是普通用户。  


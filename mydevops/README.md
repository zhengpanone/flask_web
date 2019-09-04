# mydevops

## 安装django
pip install django

## 创建项目

django-admin startproject mydevops

## 创建应用

python ./manage.py startapp scanhosts

## 创建admin用户和密码并赋予本地访问的权限
GRANT ALL ON mydevops.* TO admin@'localhost' IDENTIFIED by 'admin';
FLUSH PRIVILEGES;
 
 
 ## makemigrations生成迁移文件
 python ./manage.py makemigrations
 
 ## 迁移文件生产SQL转换为表
 python ./manage.py migrate
 
 ## 实体类
 
 ### 资产信息展示表
 #### 所属应用 detail
 ##### 表名 
 ConnectionInfo、NetConnectionInfo、PhysicalServerInfo、VirtualServerInfo、OtherMachineInfo、NetWorkInfo
 
 ### 资产信息探测表
 #### 所属应用 scanhosts
 ##### 表名
 HostLogInfo
 
 ## nmap???
 python-nmap 存活设备IP列表
 telnetlib  是否Linux服务主机IP列表
 
 pexpect
 paramiko 基于Python实现的SSH远程安全连接,用于SSH远程执行命令,文件传输等功能的ssh客户端
 
 
 
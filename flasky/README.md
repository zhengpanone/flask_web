# https://github.com/miguelgrinberg/flasky

blog    # 博客
    app
        forms
            user.py
        models # 模型
            user.py
        static # 静态文件
        templates  # 模板
            common # 基类模板
                base.html
            email
                email.html
            errors
                errors.html
            main
                index.html
            user
                login.html
                register.html
         views  # 视图蓝本
             __init__.py
             main.py
             user.py
        __init__.py
        lib
            email.py
            extensions.py # 扩展库
            settings.py # 系统配置
     migrations # 迁移文件
     manage.py  # 启动文件

# https://blog.csdn.net/weixin_41829272/article/details/80643655

# 创建迁移仓库 Flask-Migrate
## 初始化 Flask-Migrate migrate = Migrate(app,db)
### flask db init  
#### init 子命令添加数据库迁移支持

## 创建迁移脚本
在Alembic中, 数据库迁移用迁移脚本。脚本中有两个函数,分别是upgrade() 和 downgrade()。upgrade() 函数把迁移中的改动应用到数据库中，downgrade() 函数则将改动删除。Alembic 具有添加和删除改动的能力，意味着数据库可重设到修改历史的任意一点。

 ## Flask-Migrate管理数据库模式变化如下步骤
 - 对模型类做必要修改
 - 执行flask db migrate 命令,自动创建一个迁移脚本
 - 检查自动生成的脚本,根据对模型的实际改动进行调整
 - 把迁移脚本纳入版本控制
 - 执行flask db upgrade命令,把迁移应用到数据库。
 
 flask db migrate子命令用于自动创建迁移脚本
 flask db upgrade 把迁移应用到数据库中。能把改动应用到数据库中，且不影响其中保存的数据。


- Flask-Login 管理已登录用户的会话
- Werkzeug 计算密码散列值并进行核对
- itsdangerous 生成并核对加密安全令牌
- Flask-Mail 发送与身份验证相关的电子邮件
- Flask-Bootstrap HTML模板
- Flask-WTF Web表单


## Flask-Login 实现的属性和方法
- is_authenticated 如果用户登录的凭据有效,返回True,否则返回False
- is_active 如果用户登录,返回True,否则返回False。如果想禁用账户,返回False
- is_anonymous 对普通用户必须返回Flase,如果表示匿名用户的特殊对象,应该返回True
- get_id() 返回用户的唯一标识符,使用Unicode编码字符串


## 将角色添加到数据库
- flask shell
- Role.insert_roles()
- Role.query.all()


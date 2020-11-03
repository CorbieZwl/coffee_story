启动方式 :
    修改settings中mysql密码 改成自己的
    在mysql中创建数据库 coffee_server
    迁移数据脚本 python3 manage.py migrate
    ok
    admin页面
    用户名:zwl
    密码:123456

插入商品数据:
    视图函数: goods/views asdas()
    插入方式 启动服务器输入路由 http://127.0.0.1:8000/addgoodsdata  可以插入60条商品数据
    
插入用户数据:
        http://127.0.0.1:8000/adduserinfo 
        
开启celery:

celery -A coffee_server worker -l INFO 



使用ctrl+F修改ajax和settings中的ip地址为自己本机地址

邮箱验证可能过期 需要修改授权码



迁移数据库:

python3 manage.py migrate
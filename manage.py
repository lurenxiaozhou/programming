import logging

from flask  import session
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from info import create_app,db
from info.models import *
# 通过传入不同配置创造出不同配置下的app实例，工厂方法
app = create_app('develop')
# 6. 配置manager
manager = Manager(app)
# 7. 设置sql迁移
Migrate(app,db)
manager.add_command('db',MigrateCommand)


@manager.option("-n","--username",dest="username")
@manager.option("-p","--password",dest="password")
def createsuperuser(username,password):
    if not all([username,password]):
        print("参数不全")

    user = User()
    user.nick_name = username
    user.mobile = username
    user.password = password
    user.is_admin = 1

    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    print("ok")







if __name__ == "__main__":
    print()
    manager.run()
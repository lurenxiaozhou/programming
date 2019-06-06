import logging

from flask  import session
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from info import create_app,db

# 通过传入不同配置创造出不同配置下的app实例，工厂方法
app = create_app('develop')
# 6. 配置manager
manager = Manager(app)
# 7. 设置sql迁移
Migrate(app,db)
manager.add_command('db',MigrateCommand)



@app.route("/")
def index():
    # 演示log
    logging.error("error")
    logging.debug("debug")
    logging.warning("warning")
    logging.info("info")
    logging.critical("critical")

    return  "hello world"



if __name__ == "__main__":
    manager.run()
from flask  import session
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from info import app,db

# 6. 配置manager
manager = Manager(app)
# 7. 设置sql迁移
Migrate(app,db)
manager.add_command('db',MigrateCommand)



@app.route("/")
def index():
    session["hhh"]='hjhkhk'
    return  "hello world"



if __name__ == "__main__":
    manager.run()
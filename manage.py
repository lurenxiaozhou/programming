from flask  import Flask,session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate
from config import Config

app = Flask(__name__)
# 1.集成配置类
app.config.from_object(Config)
# 2.配置SQLAlchemy
db = SQLAlchemy(app)
# 3.配置redis
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)
# 4. 配置CSRFProtect
CSRFProtect(app)
# 5. 配置Session
Session(app)
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
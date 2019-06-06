from flask  import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/programming'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #redis类属性
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379


app = Flask(__name__)
# 1.集成配置类
app.config.from_object(Config)
# 2.配置SQLAlchemy
db = SQLAlchemy(app)
# 3.配置redis
redis_store = StrictRedis(host=Config.REDIS_HOST,port=Config.REDIS_PORT)



@app.route("/")
def index():
    return  "hello world"



if __name__ == "__main__":
    app.run()
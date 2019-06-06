from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from redis import  StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session


# 创建db分成两部，使用init_app
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # 1.集成配置类
    app.config.from_object(config[config_name])
    # 2.配置SQLAlchemy
    db.init_app(app)
    # 3.配置redis
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT)
    # 4. 配置CSRFProtect
    CSRFProtect(app)
    # 5. 配置Session
    Session(app)
    return app
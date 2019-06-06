from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from redis import  StrictRedis
from flask_wtf import CSRFProtect
from flask_session import Session





app = Flask(__name__)
# 1.集成配置类
app.config.from_object(config['develop'])
# 2.配置SQLAlchemy
db = SQLAlchemy(app)
# 3.配置redis
redis_store = StrictRedis(host=config['develop'].REDIS_HOST,port=config['develop'].REDIS_PORT)
# 4. 配置CSRFProtect
CSRFProtect(app)
# 5. 配置Session
Session(app)
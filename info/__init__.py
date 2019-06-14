import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from redis import  StrictRedis
from flask_wtf.csrf import CSRFProtect,generate_csrf
from flask_session import Session

from info.utils.common import do_index_class


def set_log(config_name):
    # 设置日志的记录等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)  # 调试debug级
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


# 创建db分成两部，使用init_app
db = SQLAlchemy()

# 声明他是一个StrictRedis的实例对象
redis_store = None # type: StrictRedis


def create_app(config_name):
    # 调用log日志封装的函数
    set_log(config_name)
    app = Flask(__name__)
    # 1.集成配置类
    app.config.from_object(config[config_name])
    # 2.配置SQLAlchemy
    db.init_app(app)
    # 3.配置redis
    global redis_store
    redis_store = StrictRedis(host=config[config_name].REDIS_HOST,port=config[config_name].REDIS_PORT,decode_responses=True)
    # 4. 配置CSRFProtect,只起到保护作用，具体往表单和cookie中设置csrf_token还需要我们自己去做
    # 先往cookie中添加一个csrf_token
    @app.after_request
    def after_request(response):
        # 通过wtf这个扩展给我们生成的token
        csrf_token = generate_csrf()
        response.set_cookie("csrf_token",csrf_token)
        return response
    CSRFProtect(app)
    # 5. 配置Session
    Session(app)
    # 注册蓝图
    from info.modules.index import index_blu
    app.register_blueprint(index_blu)
    from info.modules.passport import passport_blu
    app.register_blueprint(passport_blu)
    from info.modules.news import news_blu
    app.register_blueprint(news_blu)
    from info.modules.profile import profile_blu
    app.register_blueprint(profile_blu)
    # 添加过滤器
    app.add_template_filter(do_index_class,"index_class")
    return app
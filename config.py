import logging

from redis import StrictRedis



class Config(object):
    SECRET_KEY = 'dawangjiaowolaixunshan'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/programming'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #redis类属性
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    #Session配置
    #指定存储方式
    SESSION_TYPE = 'redis'
    #指定存储对象redis的地址端口
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    #设置永久保存为false
    SESSION_PERMANENT = False
    # 设置签名加密
    SESSION_USE_SIGNER = True
    #设置保存时间两天
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    # 设置数据库默认提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


# 面向对象继承
#开发环境配置
class DevelopConfig(Config):
    DEBUG = True
    LOG_LEVEL=logging.DEBUG


 # 生产环境
class ProductConfig(Config):
    LOG_LEVEL = logging.ERROR


#测试环境
class TestingConfig(Config):
    DEBUG = True


# 用字典进行封装
config = {
    "develop":DevelopConfig,
    "product":ProductConfig,
    "testing":TestingConfig
}


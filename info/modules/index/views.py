from info import redis_store
from info.modules.index import index_blu


@index_blu.route("/")
def index():
    # 测试是否设置成功
    redis_store.set('names','xiaozhou')
    return  "hello world"
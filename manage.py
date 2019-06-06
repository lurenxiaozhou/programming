from flask  import Flask


class Config(object):
    DEBUG = True


app = Flask(__name__)
# 1.集成配置类
app.config.from_object(Config)

@app.route("/")
def index():
    return  "hello world"



if __name__ == "__main__":
    app.run()
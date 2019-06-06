from flask  import Flask
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/programming'
    SQLALCHEMY_TRACK_MODIFICATIONS = True



app = Flask(__name__)
# 1.集成配置类
app.config.from_object(Config)
# 2.配置SQLAlchemy
db = SQLAlchemy(app)
@app.route("/")
def index():
    return  "hello world"



if __name__ == "__main__":
    app.run()
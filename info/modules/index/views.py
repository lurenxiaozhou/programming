from flask import render_template, send_file, current_app, redirect, session
from info.modules.index import index_blu
from info.models import User, News


@index_blu.route("/")
def index():
    # 需求：首页右上角实现
    # 当我们进入到首页。我们需要判断用户是否登录，将用户信息查出来，渲染给index.html
    user_id = session.get("user_id") #获取到当前session保存的用户
    user = None
    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    #1.显示新闻列表
    clicks_news = []
    try:
        clicks_news = News.query.order_by(News.clicks.desc()).limit(6).all()
    except Exception as e:
        current_app.logger.error(e)

    clicks_news_li = []
    # for news_obj in clicks_news:
    #     clicks_news_dict = news_obj.to_basic_dict()
    #     clicks_news_li.append(clicks_news_dict)
    # 列表推倒式
    clicks_news_li = [news_obj.to_basic_dict() for news_obj in clicks_news]

    # 如果user为空那么传一个None，如果不为空user.to_dict
    data = {
        "user_info": user.to_dict() if user else None,
        "clicks_news_li":clicks_news_li
    }

    return  render_template('news/index.html',data =data)



@index_blu.route("/favicon.ico")
def favicon():
    # 图标加载
    # return send_file("/static/news/favicon.ico")
    # redirect("/static/news/favicon.ico")
    return current_app.send_static_file("news/favicon.ico")
import constants
from info.modules.news import news_blu
from flask import render_template, session, current_app, g, abort
from info.utils.common import user_login
from info.models import News


@news_blu.route('/<int:news_id>')
@user_login
def detail(news_id):
    """
    详情页渲染
    :param news_id:
    :return:
    """
    user = g.user

    # 1.查询点击排行新闻
    clicks_news = []
    try:
        clicks_news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)
    clicks_news_li = [news.to_basic_dict() for news in clicks_news]

    # 2.显示新闻的具体信息
    if not news_id:
        abort(404) # 判断新闻id存不存在
        # 类型是不是整数类型
    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        abort(404)
    # 判断新闻是不是存在
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    if not news:
        abort(404)


    data = {
        "user_info":user.to_dict() if user else None,
        "clicks_news_li":clicks_news_li,
        "news":news.to_basic_dict()
    }
    return render_template("news/detail.html",data = data)
from info.modules.news import news_blu
from flask import render_template
@news_blu.route('/<int:news_id>')
def detail(news_id):
    """
    详情页渲染
    :param news_id:
    :return:
    """
    return render_template("news/detail.html")
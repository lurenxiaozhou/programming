from info.modules.news import news_blu
from flask import render_template,session,current_app
from info.utils.common import user_login



@news_blu.route('/<int:news_id>')
def detail(news_id):
    """
    详情页渲染
    :param news_id:
    :return:
    """
    user = user_login()
    data = {
        "user_info":user.to_dict() if user else None
    }
    return render_template("news/detail.html",data = data)
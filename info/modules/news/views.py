from info.modules.news import news_blu
from flask import render_template,session,current_app

from info.models import User


@news_blu.route('/<int:news_id>')
def detail(news_id):
    """
    详情页渲染
    :param news_id:
    :return:
    """
    user_id = session.get("user_id")
    user = None

    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
    data = {
        "user_info":user.to_dict() if user else None
    }
    return render_template("news/detail.html",data = data)
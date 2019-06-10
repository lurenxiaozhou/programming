from flask import current_app, session

from info.models import User


def do_index_class(index):
    if index == 1:
        return "first"
    elif index ==2:
        return "second"
    elif index ==3:
        return "third"
    else:
        return ""

def user_login():
    user_id = session.get("user_id")
    user = None

    if user_id:
        try:
            user = User.query.get(user_id)
        except Exception as e:
            current_app.logger.error(e)
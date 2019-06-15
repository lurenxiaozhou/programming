from flask import Blueprint

admin_blu = Blueprint("admin",__name__,url_prefix="/admin")

from .views import *


@admin_blu.before_request
def admin_identification():
    # 在每次请求前执行，获取session中的is_admin 如果能获取到就说明是
    # 如果访问的是登录界面可以进入
    is_login = request.url.endswith("/login")
    is_admin = session.get("is_admin")
    if not is_login and not is_admin:
        return redirect("/")
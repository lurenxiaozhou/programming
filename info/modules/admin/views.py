from info.modules.admin import admin_blu
from flask import render_template

@admin_blu.route("/login")
def login():
    """
    后台登录页面
    :return:
    """
    return render_template("admin/login.html")

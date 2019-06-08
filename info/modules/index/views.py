from flask import render_template, send_file, current_app, redirect
from info.modules.index import index_blu


@index_blu.route("/")
def index():


    return  render_template('news/index.html')



@index_blu.route("/favicon.ico")
def favicon():
    # 图标加载
    # return send_file("/static/news/favicon.ico")
    # redirect("/static/news/favicon.ico")
    return current_app.send_static_file("news/favicon.ico")
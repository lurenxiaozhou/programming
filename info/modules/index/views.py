from flask import render_template, current_app, request, jsonify, g
from info.modules.index import index_blu
from info.models import  News, Category
from info import constants
from utils.response_code import RET
from info.utils.common import user_login

@index_blu.route('/news_list')
def get_news_list():
    """
    1.接收参数 cid page per_page
    2.效验参数合法性
    3.查询出的新闻（要关系分类）（创建时间的排序）
    4.返回响应，返回新闻数据
    :return:
    """
    # 1.接收参数 cid page per_page
    cid = request.args.get('cid')
    page = request.args.get('page',1)
    per_page = request.args.get('per_page',10)
    # 2.效验参数合法性
    try:
        cid = int(cid)
        page = int(page)
        per_page = int(per_page)
    except Exception as e:
        current_app.logger.error(e)
        return  jsonify(errno = RET.PARAMERR,errmsg = "参数错误")
    # 3.查询出的新闻（要关系分类）（创建时间的排序）
    filters = []
    if cid != 1:
        filters.append(News.category_id == cid)
    # 把空列表变空  *[]解包
    try:
        paginate=News.query.filter(*filters).order_by(News.create_time.desc()).paginate(page,per_page,False)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "数据库查询错误")
    news_list = paginate.items # [obj,obj]
    current_page = paginate.page
    total_page = paginate.pages

    news_dict_li =[]
    for news in news_list:
        news_dict_li.append(news.to_basic_dict())
    data={
        "news_dict_li":news_dict_li,
        "current_page":current_page,
        "total_page":total_page
    }

    return jsonify(errno = RET.OK,errmsg = "OK",data = data)


@index_blu.route("/")
@user_login
def index():
    # 需求：首页右上角实现
    # 当我们进入到首页。我们需要判断用户是否登录，将用户信息查出来，渲染给index.html
    user = g.user
    #1.显示新闻列表
    clicks_news = []
    try:
        clicks_news = News.query.order_by(News.clicks.desc()).limit(constants.CLICK_RANK_MAX_NEWS).all()
    except Exception as e:
        current_app.logger.error(e)

    clicks_news_li = []
    # for news_obj in clicks_news:
    #     clicks_news_dict = news_obj.to_basic_dict()
    #     clicks_news_li.append(clicks_news_dict)
    # 列表推倒式
    clicks_news_li = [news_obj.to_basic_dict() for news_obj in clicks_news]
    # 2.显示新闻分类
    categorys = []
    try:
        categorys = Category.query.all()  # [obj,obj]
    except Exception as e:
        current_app.logger.error(e)
    categorys_li = []
    # [obj,obj] ---> [{},{}]
    categorys_li = [category.to_dict() for category in categorys]
    # 如果user为空那么传一个None，如果不为空user.to_dict
    data = {
        "user_info": user.to_dict() if user else None,
        "clicks_news_li":clicks_news_li,
        "categorys":categorys_li
    }


    return  render_template('news/index.html',data =data)



@index_blu.route("/favicon.ico")
def favicon():
    # 图标加载
    # return send_file("/static/news/favicon.ico")
    # redirect("/static/news/favicon.ico")
    return current_app.send_static_file("news/favicon.ico")
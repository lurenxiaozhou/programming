
from info import db,constants
from info.modules.news import news_blu
from flask import render_template, session, current_app, g, abort, jsonify, request
from info.utils.common import user_login
from info.models import News, Comment, CommentLike, User
from info.utils.response_code import RET


@news_blu.route('/followed_user', methods=["POST"])
@user_login
def followed_user():
    """
    关注取消关注
    :return:
    """
    if not g.user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    user_id = request.json.get("user_id")
    action = request.json.get("action")

    if not all([user_id, action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    if action not in ("follow", "unfollow"):
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    # 查询到关注的用户信息
    try:
        target_user = User.query.get(user_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="查询数据库失败")

    if not target_user:
        return jsonify(errno=RET.NODATA, errmsg="未查询到用户数据")

    # 根据不同操作做不同逻辑
    if action == "follow":
        if target_user.followers.filter(User.id == g.user.id).count() > 0:
            return jsonify(errno=RET.DATAEXIST, errmsg="当前已关注")
        target_user.followers.append(g.user)
    else:
        if target_user.followers.filter(User.id == g.user.id).count() > 0:
            target_user.followers.remove(g.user)

    # 保存到数据库
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据保存错误")

    return jsonify(errno=RET.OK, errmsg="操作成功")








@news_blu.route('/comment_like',methods = ["POST"])
@user_login
def set_comment_like():
    """
    点赞和取消点赞
    1.接收参数 comment_id action
    2.效验参数
    3.CommentLike()往点赞的表中添加或删除一条数据
    4.返回响应
    :return:
    """
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    comment_id = request.json.get("comment_id")
    action = request.json.get("action")

    if not all([comment_id,action]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if not action in ['add','remove']:
        return jsonify(errno = RET.PARAMERR,errmsg = "参数错误")

    try:
        comment_id = int(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.PARAMERR,errmsg = "参数错误")

    try:
        comment_obj = Comment.query.get(comment_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "数据库查询错误")

    if not comment_obj:
        return jsonify(errno = RET.NODATA,errmsg = "该条评论不存在")

    comment_like_obj = CommentLike.query.filter_by(comment_id=comment_id,user_id = user.id).first()
    # 业务逻辑
    if action == "add":
        if not comment_like_obj:
            # 点赞
            comment_like = CommentLike()
            comment_like.comment_id = comment_id
            comment_like.user_id = user.id
            db.session.add(comment_like)
            comment_obj.like_count += 1
    else:
        # 如果点赞存在，才删除
        if comment_like_obj:
            db.session.delete(comment_like_obj)
            comment_obj.like_count -= 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "数据库操作失败")

    return jsonify(errno = RET.OK,errmsg = "OK")






@news_blu.route('/news_comment',methods=["POST"])
@user_login
def news_comment():
    """
    新闻评论功能
    1.接收参数 用户 新闻 评论内容 parant_id
    2.效验参数
    3.业务逻辑 往数据库中添加一条评论
    4. 返回响应 返回响应烦人评论
    :return:
    """
    #  用户登录状态
    user = g.user
    if not user:
        return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")
    # 接收参数
    news_id = request.json.get("news_id")
    comment_str = request.json.get("comment")
    parent_id = request.json.get("parent_id")
    # 效验参数
    if not all([news_id,comment_str]):
        return jsonify(errno = RET.PARAMERR,errmsg = "参数错误")
    try:
        news_id = int(news_id)
        if parent_id:
            parent_id = int(parent_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.PARAMERR,errmsg = "参数类型错误")
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "数据库查询错误")
    if not news:
        return jsonify(errno = RET.NODATA,errmsg = "该条新闻不存在")
    # 添加新闻评论
    comment = Comment()
    comment.user_id = user.id
    comment.news_id = news_id
    comment.content = comment_str
    if parent_id:
        comment.parent_id = parent_id
    try:
        db.session.add(comment)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "数据库保存错误")
    return jsonify(errno = RET.OK,errmsg = "OK",data=comment.to_dict())


@news_blu.route('/news_collect',methods=["POST"])
@user_login
def news_collect():
    """
    新闻的收藏与取消收藏
    1.接收参数
    2.效验参数
    3.收藏新闻和取消收藏
    4.返回响应
    :return:
    """
    # 用户登录状态
    user = g.user
    if not user:
        return jsonify(errno = RET.SESSIONERR,errmsg = "用户未登录")
    # 接收参数
    news_id = request.json.get("news_id")
    action = request.json.get("action")
    # 效验参数
    if not all([news_id,action]):
        return jsonify(errno = RET.PARAMERR,errmsg = "参数错误")
    if action not in ['collect', 'cancel_collect']:
        return jsonify(errno = RET.PARAMERR,errmsg = "参数错误")
    try:
        news_id = int(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.PARAMERR,errmsg = "数据格式不正确")
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DBERR,errmsg = "数据库查询失败")
    if not news:
        return jsonify(errno = RET.NODATA,errmsg = "该条新闻不存在")

    #收藏新闻和取消收藏
    if action == "collect":
        # 当去们去收藏当前新闻的时候要判断他是否已经收藏过了，收藏过就不在收藏
        if news not in user.collection_news:
            user.collection_news.append(news)
    else:
        # 当去取消的时候判断他是否在收藏列表中，
        if news in user.collection_news:
            user.collection_news.remove(news)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        db.session.rollback()
        return jsonify(errno=RET.DBERR, errmsg="保存失败")
    return jsonify(errno = RET.OK,errmsg = "OK")



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
    # if not news_id:
    #     abort(404) # 判断新闻id存不存在
    #     # 类型是不是整数类型
    # try:
    #     news_id = int(news_id)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     abort(404)
    # 判断新闻是不是存在
    news = None
    try:
        news = News.query.get(news_id)
    except Exception as e:
        current_app.logger.error(e)

    if not news:
        abort(404)
    # 访问点击量加1
    news.clicks += 1

    # 详情页收藏是由is_collected控制的
    is_collected = False
    # 用户如果收藏了该新闻就让is_collected=True
    # 1. 保证用户存在
    # 2. 新闻肯定存在
    # 3. 该条新闻在用户收藏新闻的列表中
    # 4.用户收藏新闻的列表 -----》user.collection_news.all()  [news, news]
    if user and news in user.collection_news.all():
        is_collected = True

    #  查询出当前新闻的评论
    comments = []
    try:
        comments = Comment.query.filter(Comment.news_id == news_id).order_by(Comment.create_time.desc()).all()
    except Exception as e:
        current_app.logger.error(e)

    # comments_dict_li = [comment.to_dict() for comment in comments]
    comment_like_ids =[]
    if user:
        comment_ids = [comment.id for comment in comments]
        comment_likes = CommentLike.query.filter(CommentLike.user_id == user.id,CommentLike.comment_id.in_(comment_ids)).all()
        comment_like_ids = [comment_like.comment_id for comment_like in comment_likes]

    comments_dict_li=[]
    for comment in comments:
        comment_dict = comment.to_dict()
        comment_dict["is_like"] = False
        # 如果comment_dict["is_like"] = True代表以赞
        # 如果该条评论的id在我的点赞评论id列表中
        if comment.id in comment_like_ids:
            comment_dict["is_like"] = True
        comments_dict_li.append(comment_dict)

    # 当前登录用户是否关注该作者
    is_followed = False
    if user and news.user.followers.filter(User.id == g.user.id).count() > 0:
        is_followed = True





    data = {
        "user_info":user.to_dict() if user else None,
        "clicks_news_li":clicks_news_li,
        "news":news.to_dict(),
        "is_collected":is_collected,
        "comments_dict_li":comments_dict_li,
        "is_followed":is_followed
    }
    return render_template("news/detail.html",data = data)
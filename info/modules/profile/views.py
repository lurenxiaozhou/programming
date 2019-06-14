from flask import g, redirect,render_template,request,jsonify,current_app

from info import constants
from info import db
from info.modules.profile import profile_blu
from info.utils.common import user_login
from info.libs.image_storage import storage
from utils.response_code import RET


@profile_blu.route('/user/user_pic_info',methods = ["GET","POST"])
@user_login
def user_pic_info():
    """
    用户图片设置
    :return:
    """
    user = g.user
    if request.method == "GET":
        data = {
            "user_info":user.to_dict()
        }

        return render_template("news/user_pic_info.html",data =data)

    try:
        image_data = request.files.get("avatar").read()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    #上传图片
    try:
        key = storage(image_data)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="上传头像失败")

    user.avatar_url = key

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存数据库失败")

    return jsonify(errno=RET.OK, errmsg="上传头像成功",data = constants.QINIU_DOMIN_PREFIX + key)



@profile_blu.route('/user_base_info',methods = ["GET","POST"])
@user_login
def user_base_info():
    """
    宣言基本资料界面
    :return:
    """
    user = g.user
    if request.method == "GET":
        data = {
            "user_info":user.to_dict()
        }

        return render_template("news/user_base_info.html",data = data)

    nick_name = request.json.get("nick_name")
    signature = request.json.get("signature")
    gender = request.json.get("gender")

    if not all([nick_name,signature,gender]):
        return jsonify(errno=RET.PARAMERR, errmsg="参数不完整")

    if gender not in ['MAN','WOMAN']:
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    user.nick_name = nick_name
    user.signature = signature
    user.gender = gender

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.PARAMERR, errmsg="参数错误")

    return jsonify(errno=RET.OK, errmsg="OK",data = user.to_dict())


@profile_blu.route('/info')
@user_login
def user_info():
    """
    渲染个人中心页面
    :return:
    """

    user = g.user
    if not user:
        return redirect('/')

    data={
        "user_info":user.to_dict()
    }
    return render_template("news/user.html",data=data)
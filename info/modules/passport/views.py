import random
import re

import constants
from info import redis_store
from info.modules.passport import passport_blu
from flask import request, abort, current_app, make_response, jsonify

from libs.yuntongxun.sms import CCP

from utils.captcha.captcha import captcha
from utils.response_code import RET


@passport_blu.route('/sms_code',methods = ['POST'])
def get_sms_code():
    """
    1.接收参数mobile，image_code，image_code_id
    2.效验参数：mobile 用正则
    3.效验用户输入的验证码和通过image_code_id查询redis的是否一致
    :return:
    """

    #json数据接收
    dict_data = request.json
    # 1.接收参数
    mobile = dict_data.get("mobile")
    image_code = dict_data.get("image_code")
    image_code_id = dict_data.get("image_code_id")
    # 2.全局参数判断
    if not all([mobile,image_code,image_code_id]):
        return jsonify(errno = RET.PARAMERR,errsms = "有参数为空")
    # 3.判断电话号码是否符合
    if not re.match(r"1[35678][0-9]{9}$",mobile):
        return jsonify(errno = RET.DATAERR,errsms = "号码不符合")
    # 4.验证输入的验证码是否正确
    try:
        real_image_code = redis_store.get("ImageCodeId_"+image_code_id)
        # 如果取出来值则删除数据库中的数据
        if real_image_code:
            real_image_code = real_image_code.decode()
            redis_store.delete("ImageCodeId_"+image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DATAERR,errsms = "获取图片失败")
    # 5.验证码过期，为空
    if not real_image_code:
        return jsonify(errno = RET.DATAERR,errsms = "验证码过期")
    # 6.判断两个验证码是否匹配
    if image_code.lower() != real_image_code.lower():
        return jsonify(errno = RET.DATAERR,errsms = "输入验证码不匹配")

    # 7.效验手机号是否已经被注册
    try:
        from models import User
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DATAERR,errsms = "数据库错误")
    if user:
        return jsonify(errno = RET.DATAEXIST,errsms = "该手机已经注册")
    # 8.生成验证码并发送短信
    result = random.randint(0,999999)
    sms_code = "%06d" %result
    current_app.logger.debug("短信验证内容%s"%sms_code)
    result =CCP().send_template_sms(mobile,[sms_code,constants.SMS_CODE_REDIS_EXPIRES/60],"1")
    if result != 0:
        return jsonify(errno = RET.DATAERR,errsms = "发送失败")
    # 9.redis 中保存短信验证码内容
    try:
        redis_store.set("sms_"+mobile,sms_code,constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno = RET.DATAERR,errsms = "保存失败")
    # 10 返回发送成功的响应
    return jsonify(errno = RET.OK,errsms = "发送成功")












@passport_blu.route('/image_code')
def get_image_code():

    # 1.获取到当前的图片编号id
    image_code_id = request.args.get('imageCodeId')

    # 2.效验参数是否存在
    if not image_code_id:
        abort(404)

    # 3.生成验证码 captche
    _,text,image = captcha.generate_captcha()

    # 4.把随机的字符串和生成的文本验证码以key，value的形式保存到redis
    try:
        redis_store.setex("ImageCodeId_"+image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES,text)
    except Exception as e:
        current_app.logger.error(e)
        abort(500)

    response = make_response(image)
    response.headers["Content-Type"]="image/jpg"
    return response

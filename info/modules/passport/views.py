import constants
from info import redis_store
from info.modules.passport import passport_blu
from flask import request, abort, current_app, make_response

from utils.captcha.captcha import captcha


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

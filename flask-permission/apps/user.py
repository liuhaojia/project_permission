from apps import db
from orm.model import User
from utils import MD5Util
from flask import Blueprint, request, make_response, jsonify, current_app
from sqlalchemy import or_, and_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 创建一个蓝图，蓝图名称 user，前缀 /user
user_dp = Blueprint("user", __name__, url_prefix="/user")


# 后面写API接口 =============================================================


def create_token(api_user):
    '''
    生成token
    :param api_user:用户id
    :return: token
    '''

    # 第一个参数是内部的私钥，这里写在共用的配置信息里了，如果只是测试可以写死
    # 第二个参数是有效期(秒)
    s = Serializer(current_app.config["SECRET_KEY"], expires_in=3600)
    # 接收用户id转换与编码
    print(api_user)
    token = s.dumps({"id": api_user})
    return token


# 登录判断
@user_dp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # 获取用户名和密码，并密码加密
        username = request.json['username']
        password = request.json['password']
        password = MD5Util.md5vale(password)

        # 将用户名和加密后的密码去数据库查询
        user = db.session.query(User).filter(and_(
            User.username == username,
            User.password == password
        )).first()
        print(user)

        result = {}
        if user is not None:  # 登录成功
            # 设置cookie？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
            # 未做
            result["flag"] = True
            result["msg"] = "登录成功"
            result["data"] = user.to_json()
            print(user.id)
            print(create_token(user.id))
        else:   # 登录失败
            result["flag"] = False
            result["msg"] = "登录失败"

        print(result["msg"])

        # 解决前后端分离跨域问题
        rst = make_response(jsonify(result))
        # rst.headers['Access-Control-Allow-Origin'] = '*'  # 任意域名
        # if request.method == 'POST':
        #     rst.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
        return rst

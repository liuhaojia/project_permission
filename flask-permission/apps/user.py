from apps import db
from orm.model import User, Role, tab_user_role
from utils import MD5Util
from flask import Blueprint, request, make_response, jsonify, current_app, app
from sqlalchemy import or_, and_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import session, Response

# 创建一个蓝图，蓝图名称 user，前缀 /user
user_dp = Blueprint("user", __name__, url_prefix="/user")


# 后面写API接口 =============================================================
@user_dp.after_request
def af_req(resp):  # 解决跨域session丢失
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = 'http://localhost:8080'
    resp.headers['Access-Control-Allow-Methods'] = 'PUT,POST,GET,DELETE,OPTIONS'
    # resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Content-Length, Authorization, Accept, ' \
                                                   'X-Requested-With , yourHeaderFeild '
    resp.headers['Access-Control-Allow-Credentials'] = 'true'

    resp.headers['X-Powered-By'] = '3.2.1'
    resp.headers['Content-Type'] = 'application/json;charset=utf-8'
    return resp


def create_token(uid, scope=None, expiration=5000):
    # 通过flask提供的对象，传入过期时间和flask的SECRET_KEY
    """生成令牌"""
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    # token里面的值，是技术方案需要订的，做相关的业务逻辑验证，uid唯一值表示当前请求的客户端
    # type表示客户端类型，看业务场景进行增删
    # scope权限作用域
    # 设置过期时间，这个是必须的，一般设置两个小时
    return s.dumps({
        'uid': uid,
        # 'type': type.value,
        'scope': scope
    }).decode('ascii')


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
        # 查询角色
        print(user)

        result = {}
        data = {}
        if user is not None:  # 登录成功
            result["flag"] = True
            result["msg"] = "登录成功"
            data["token"] = create_token(user.id)

            # result["data"] = user.to_json()
            result["data"] = data
            result["code"] = 1
        else:   # 登录失败
            result["flag"] = False
            result["msg"] = "登录失败123"

        print(result["msg"])

        # 解决前后端分离跨域问题
        rst = make_response(jsonify(result))
        # rst.headers['Access-Control-Allow-Origin'] = '*'  # 任意域名
        # if request.method == 'POST':
        #     rst.headers['Access-Control-Allow-Methods'] = 'POST'  # 响应POST
        return rst


def verify_token(token):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        # 转换为字典
        user_id = s.loads(token)

    except Exception:
        return None
    return user_id


@user_dp.route('/info')
def info():
    token = request.headers["Authorization"]
    user_id = verify_token(token)
    if user_id:
        print(user_id["uid"])

        data = {
            "avatar": "https://randy168.com/1533262153771.gif",
            "roles": ["admin", ],
            "data": ["order-manage", "order-list", "product-manage", "product-list", "review-manage", "return-goods",
                     "goods", "goods-list",  "goods-classify", "permission", "user-manage", "role-manage", "menu-manage"]
        }
        return {
            "code": 1,
            "data": data
        }
    else:
        return "登录失败"

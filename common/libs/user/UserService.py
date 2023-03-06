import base64
import hashlib
import random
import string


class UserService:
    @staticmethod
    def genePwd(pwd, salt):
        """
        密码加密
        :param pwd: 密码明文
        :param salt: 密码加密动态码
        :return: 加密后的密码
        """
        m = hashlib.md5()
        str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneAuthCode(user_info):
        """
        认证码
        :param user_info: 用户对象
        :return: 加密后的cookie
        """
        m = hashlib.md5()
        str = "%s-%s-%s-%s" % (user_info.uid, user_info.login_name, user_info.login_pwd, user_info.login_salt)
        return m.hexdigest()

    @staticmethod
    def geneSalt(length=16):
        key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return ("".join(key_list))

import hashlib
import os
import time
from peewee import *
from slim.base.user import BaseUser
from slim.utils import StateObject, get_bytes_from_blob

import config
from model import BaseModel, db


class POST_STATE(StateObject):
    DEL = 0
    APPLY = 20  # 等待发布审核
    CLOSE = 30  # 禁止回复
    NORMAL = 50

    txt = {DEL: "删除", APPLY: '待审核', CLOSE: "锁定", NORMAL: "正常"}


class User(BaseModel, BaseUser):
    email = TextField(index=True, unique=True, null=True, default=None)
    nickname = TextField(index=True, unique=True, null=True)

    password = BlobField()
    salt = BlobField()

    time = BigIntegerField()  # 创建时间
    state = IntegerField(default=POST_STATE.NORMAL, index=True)  # 当前状态

    class Meta:
        db_table = 'user'

    @property
    def roles(self):
        """
        BaseUser.roles 的实现，返回用户可用角色
        :return:
        """
        ret = {None}
        if self.state == POST_STATE.DEL:
            return ret
        ret.add('user')
        return ret

    @classmethod
    def gen_password_and_salt(cls, password_text):
        """ 生成加密后的密码和盐 """
        salt = os.urandom(32)
        dk = hashlib.pbkdf2_hmac(
            config.PASSWORD_HASH_FUNC_NAME,
            password_text.encode('utf-8'),
            salt,
            config.PASSWORD_HASH_ITERATIONS,
        )
        return {'password': dk, 'salt': salt}

    def set_password(self, new_password):
        """ 设置密码 """
        info = self.gen_password_and_salt(new_password)
        self.password = info['password']
        self.salt = info['salt']
        self.save()

    def _auth_base(self, password_text):
        """
        已获取了用户对象，进行密码校验
        :param password_text:
        :return:
        """
        dk = hashlib.pbkdf2_hmac(
            config.PASSWORD_HASH_FUNC_NAME,
            password_text.encode('utf-8'),
            get_bytes_from_blob(self.salt),
            config.PASSWORD_HASH_ITERATIONS
        )

        if self.password == dk:
            return self

    @classmethod
    def auth_by_mail(cls, email, password_text):
        try: u = cls.get(cls.email == email)
        except DoesNotExist: return False
        return u._auth_base(password_text)

    @classmethod
    def auth_by_nickname(cls, nickname, password_text):
        try: u = cls.get(cls.nickname == nickname)
        except DoesNotExist: return False
        return u._auth_base(password_text)

    def __repr__(self):
        if isinstance(self.id, (bytes, memoryview)):
            return '<User id:%x nickname:%r>' % (int.from_bytes(get_bytes_from_blob(self.id), 'big'), self.nickname)
        elif isinstance(self.id, int):
            return '<User id:%d nickname:%r>' % (self.id, self.nickname)
        else:
            return '<User id:%s nickname:%r>' % (self.id, self.nickname)

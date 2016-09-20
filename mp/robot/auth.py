# -*- coding: utf-8 -*-

from mp.model import UserModel, ModNetworkModel


class Auth(object):

    def __init__(self):
        self.reg_cmd = u'我叫'

    def get_user(self, from_id):
        return UserModel.get_user_by_mapping(
                ModNetworkModel.WECHAT.network_id,
                from_id)

    def _block_username(self, username):
        # TODO
        pass

    def parse_username(self, message):
        username = message.replace(self.reg_cmd).strip()
        if self._block_username(username):
            return None

        return username and username or None

    def register_user(self, from_id, username):
        if not username:
            return u'名字不合法'

        user = UserModel()
        user.username = username
        user.save()
        user.wechat = from_id
        user.update()
        return u'注册成功！欢迎{username}'.format(username=username)

# -*- coding: utf-8 -*-

from object_model import ObjectModel


class WeChatUserModel(ObjectModel):

    table_name = 'wechat_user'

    def __init__(self, *args, **kwargs):
        super(WeChatUserModel, self).__init__(*args, **kwargs)

    @classmethod
    def get_all_sub_types(cls):
        raise (cls.DEFAULT_SUB_TYPE, )

    def _get_username(self):
        return self.get_data_field('username')
    def _set_username(self, username):
        return self.set_data_field('username', username)
    username = property(_get_username, _set_username)

    def _get_password(self):
        return self.get_data_field('password')
    def _set_password(self, password):
        return self.set_data_field('password', password)
    password = property(_get_password, _set_password)

    def _get_phone(self):
        return self.get_data_field('phone')
    def _set_phone(self, phone):
        return self.set_data_field('phone', phone)
    phone = property(_get_phone, _set_phone)

    def _get_is_admin(self):
        return self.get_data_field('is_admin', 0)
    def _set_is_admin(self, is_admin):
        return self.set_data_field('is_admin', is_admin)
    is_admin = property(_get_is_admin, _set_is_admin)

    def _get_wechat_id(self):
        return self.get_data_field('wechat_id')
    def _set_wechat_id(self, wechat_id):
        return self.set_data_field('wechat_id', wechat_id)
    wechat_id = property(_get_wechat_id, _set_wechat_id)

    def _get_ok_robot(self):
        return self.get_data_field('ok_robot', True)
    def _set_ok_robot(self, ok_robot):
        return self.set_data_field('ok_robot', ok_robot)
    ok_robot = property(_get_ok_robot, _set_ok_robot)

    def _get_rename_count(self):
        return self.get_data_field('rename_count', 1)
    def _set_rename_count(self, rename_count):
        return self.set_data_field('rename_count', int(rename_count))
    rename_count = property(_get_rename_count, _set_rename_count)

# -*- coding: utf-8 -*-

from .mod_map_model import ModMapModel
from .mod_network_model import ModNetworkModel
from .object_model import ObjectModel


class UserModel(ObjectModel):

    table_name = 'user'

    def __init__(self, *args, **kwargs):
        super(UserModel, self).__init__(*args, **kwargs)

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

    def _get_ok_robot(self):
        return self.get_data_field('ok_robot', True)
    def _set_ok_robot(self, ok_robot):
        return self.set_data_field('ok_robot', ok_robot)
    ok_robot = property(_get_ok_robot, _set_ok_robot)

    # wechat app_id unique wechat_id
    def _get_wechat(self):
        return self.get_data_field('wechat_id')
    def _set_wechat(self, wechat_id):
        old_wechat_id = self.get_data_field('wechat_id')
        if wechat_id == old_wechat_id:
            return self
        self.unlink_wechat(old_wechat_id)
        self.link_wechat(wechat_id)
        return self.set_data_field('wechat_id', wechat_id)
    wechat = property(_get_wechat, _set_wechat)

    def link_wechat(self, wechat_id):
        assert self.id
        return  ModMapModel.link(ModNetworkModel.WECHAT.network_id, wechat_id,
                ModNetworkModel.USER_SPACE.network_id, self.id)

    def unlink_wechat(self, wechat_id):
        return  ModMapModel.unlink(ModNetworkModel.WECHAT.network_id, wechat_id,
                ModNetworkModel.USER_SPACE.network_id)

    @classmethod
    def get_user_by_mapping(cls, from_network_type_id, from_network_internal_id):
        mmm = ModMapModel.one_by_from_network(from_network_type_id,
                from_network_internal_id,
                ModNetworkModel.USER_SPACE.network_id)
        if mmm is None or mmm.to_network_internal_id is None:
            return None

        return UserModel.single(mmm.to_network_internal_id)

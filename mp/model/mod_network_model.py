# -*- coding: utf8 -*-

from .id_model import IdModel


class ModNetworkPair(object):
    def __init__(self, network_id, network_name):
        self.network_id = network_id
        self.network_name = network_name

    def __repr__(self):
        return '{network_name}({network_id})'.format(network_name=self.network_name,
                network_id=self.network_id)


class ModNetworkModel(IdModel):
    table_name = 'mod_network'

    USER_SPACE = ModNetworkPair(1, 'user_space')
    USERNAME = ModNetworkPair(100, 'username')
    EMAIL = ModNetworkPair(103, 'email')
    CELLPHONE = ModNetworkPair(104, 'cellphone')
    WECHAT = ModNetworkPair(105, 'wechat')

    def __init__(self, *args, **kwargs):
        super(ModNetworkModel, self).__init__(*args, **kwargs)

    def save(self):
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()

    def delete(self):
        raise NotImplementedError()

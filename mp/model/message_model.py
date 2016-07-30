# -*- coding: utf-8 -*-

from .object_model import ObjectModel


class MessageModel(ObjectModel):

    table_name = 'message'

    SUB_TYPE_ALL = range(0, 2)
    (
        SUB_TYPE_TEXT,
        SUB_TYPE_IMAGE
    ) = SUB_TYPE_ALL

    def __init__(self, *args, **kwargs):
        super(MessageModel, self).__init__(*args, **kwargs)

    def _get_user_id(self):
        return self.parent_id
    def _set_user_id(self, user_id):
        self.parent_id = user_id
        return self
    user_id = property(_get_user_id, _set_user_id)

    @classmethod
    def get_all_sub_types(cls):
        return MessageModel.SUB_TYPE_ALL

    def _get_content(self):
        return self.get_data_field('content')
    def _set_content(self, content):
        return self.set_data_field('content', content)
    content = property(_get_content, _set_content)

    def _get_replay(self):
        return self.get_data_field('replay')
    def _set_replay(self, replay):
        return self.set_data_field('replay', replay)
    replay = property(_get_replay, _set_replay)

    # wechat_xml FromUserName
    def _get_wechat_id(self):
        return self.get_data_field('wechat_id')
    def _set_wechat_id(self, wechat_id):
        return self.set_data_field('wechat_id', wechat_id)
    wechat_id = property(_get_wechat_id, _set_wechat_id)

    def _get_pic_url(self):
        return self.get_data_field('pic_url')
    def _set_pic_url(self, pic_url):
        return self.set_data_field('pic_url', pic_url)
    pic_url = property(_get_pic_url, _set_pic_url)

    def _get_media_id(self):
        return self.get_data_field('media_id')
    def _set_media_id(self, media_id):
        return self.set_data_field('media_id', media_id)
    media_id = property(_get_media_id, _set_media_id)

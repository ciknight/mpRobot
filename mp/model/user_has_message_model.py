# -*- coding: utf8 -*-

from .relationship_model import RelationshipModel


class UserHasMessageModel(RelationshipModel):
    table_name = 'user_has_message'

    def __init__(self, *args, **kwargs):
        super(UserHasMessageModel, self).__init__(*args, **kwargs)

    def _get_user_id(self):
        return self._get_from_id()
    def _set_user_id(self, id):
        return self._set_from_id(id)
    user_id = property(_get_user_id, _set_user_id)

    def _get_message_id(self):
        return self._get_message_id()
    def _set_message_id(self, id):
        return self._set_to_id(id)
    message_id = property(_get_message_id, _set_message_id)

    @property
    def video(self):
        if self._video is None: self._video = VideoModel.single(self.video_id)
        return self._video

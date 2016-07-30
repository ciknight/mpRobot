# -*- coding: utf-8 -*-

from .parser import Parser


class MPMessageModel(object):

    TYPE_TEXT= 'text'

    def __init__(self, *args, **kwargs):
        super(MPMessageModel, self).__init__()
        self._to_username = kwargs.get('ToUserName')
        self._from_username = kwargs.get('FromUserName')
        self._create_time = kwargs.get('CreateTime')
        self._type = kwargs.get('MsgType')
        self._message = kwargs.get('Content')
        self._msg_id = kwargs.get('MsgId')

    @property
    def support_type(self):
        return (self.TYPE_TEXT, )

    @property
    def to_username(self):
        return self._to_username
    @to_username.setter
    def to_username(self, to_username):
        self._to_username = str(to_username)
        return self

    @property
    def from_username(self):
        return self._from_username
    @from_username.setter
    def from_username(self, from_username):
        self._from_username = str(from_username)
        return self

    @property
    def create_time(self):
        return self._create_time
    @create_time.setter
    def create_time(self, create_time):
        self._create_time = int(create_time)
        return self

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, type):
        self._type = str(type)
        return self

    @property
    def message(self):
        return self._message
    @message.setter
    def message(self, message):
        self._message = str(message)
        return self

    @property
    def msg_id(self):
        return self._msg_id
    @msg_id.setter
    def msg_id(self, msg_id):
        self._msg_id = str(msg_id)
        return self

    @classmethod
    def factory(cls, **kwargs):
        return MPMessageModel(**kwargs)

    @classmethod
    def parser(cls, xml_content):
        parser_dict =  Parser.xml_to_dict(xml_content)
        return cls.factory(**parser_dict)

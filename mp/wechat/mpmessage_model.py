# -*- coding: utf-8 -*-

from .parser import Parser


class MPMessageModel(object):

    TYPE_TEXT= 'text'

    def __init__(self, *args, **kwargs):
        super(MPMessageModel, self).__init__()
        self._to_id = kwargs.get('ToUserName')
        self._from_id = kwargs.get('FromUserName')
        self._create_time = kwargs.get('CreateTime')
        self._type = kwargs.get('MsgType')
        self._message = kwargs.get('Content')
        self._msg_id = kwargs.get('MsgId')
        self._encrypt = kwargs.get('Encrypt')
        self._replay = None

    @property
    def support_type(self):
        return (self.TYPE_TEXT, )

    @property
    def to_id(self):
        return self._to_id
    @to_id.setter
    def to_id(self, to_id):
        self._to_id = str(to_id)
        return self

    @property
    def from_id(self):
        return self._from_id
    @from_id.setter
    def from_id(self, from_id):
        self._from_id = str(from_id)
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

    @property
    def replay(self):
        return self._replay
    @replay.setter
    def replay(self, replay):
        self._replay = replay
        return self

    @property
    def encrypt(self):
        return self._encrypt

    @classmethod
    def factory(cls, **kwargs):
        return MPMessageModel(**kwargs)

    @classmethod
    def parser(cls, xml_content):
        parser_dict =  Parser.xml_to_dict(xml_content)
        return cls.factory(**parser_dict)

    def to_xml(self):
        _dict = dict(
            ToUserName=self.from_id,
            FromUserName=self.to_id,
            CreateTime=self.create_time,
            MsgType=self.type)
        if self.type == 'text':
            _dict.update(Content=self.replay)

        return Parser.dict_to_xml(_dict)

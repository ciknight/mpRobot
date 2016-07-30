# -*- coding: utf-8 -*-

from database_model import DataBaseModel


class IdModel(DataBaseModel):

    def __init__(self, *args, **kwargs):
        super(IdModel, self).__init__()
        self._id = kwargs.get('id')

    @property
    def id(self):
        return self._id

    @classmethod
    def fetchone(cls, row_id):
        sql = 'SELECT * FROM {table_name} WHERE `id`=%s'.format(
                table_name=cls.table_name)
        with cls.get_connection() as cursor:
            cursor.execute(sql, (row_id,))
            return cursor.fetchone()

    @classmethod
    def single(cls, row_id):
        return cls.factory(cls.fetchone(row_id=row_id))

# -*- coding: utf8 -*-

import datetime

from .database_model import DataBaseModel


class RelationshipModel(DataBaseModel):
    def __init__(self, *args, **kwargs):
        super(RelationshipModel, self).__init__()
        self._from_id = kwargs.get('from_id')
        self._to_id = kwargs.get('to_id')
        self._sequence = kwargs.get('sequence', 0)
        self._created_at = kwargs.get('created_at')

    def _get_from_id(self):
        return self._from_id
    def _set_from_id(self, from_id):
        self._from_id = long(from_id)
        return self
    from_id = property(_get_from_id, _set_from_id)

    def _get_to_id(self):
        return self._to_id
    def _set_to_id(self, to_id):
        self._to_id = long(to_id)
        return self
    to_id = property(_get_to_id, _set_to_id)

    def _get_sequence(self):
        return self._sequence
    def _set_sequence(self, sequence):
        self._sequence = int(sequence)
        return self
    sequence = property(_get_sequence, _set_sequence)

    def _get_created_at(self):
        return self._created_at
    def _set_created_at(self, created_at):
        self._created_at = created_at
        return self

    def save(self, created_at=None):
        self.created_at = datetime.datetime.now()
        sql = '''REPLACE INTO {table_name}
        (`from_id`, `to_id`, `sequence`, `created_at`)
        VALUES(%s, %s, %s, %s)'''.format(table_name=self.table_name)
        with self.get_connection() as cursor:
            cursor.execute(sql, (
                self.from_id,
                self.to_id,
                self.sequence,
                self.created_at, ))
        self.post_save()

    def update(self):
        return self.save()

    def delete(self):
        sql = '''DELETE FROM {table_name}
        WHERE `from_id`=%s AND `to_id`=%s'''.format(table_name=self.table_name)
        with self.get_connection() as cursor:
            cursor.execute(sql, (self.from_id, self.to_id, ))
        self.post_delete()

    def post_save(self):
        pass

    def post_delete(self):
        pass

    @classmethod
    def link(cls, from_id, to_id, sequence=0, created_at=None):
        assert from_id and to_id
        instance = cls()
        instance.from_id = from_id
        instance.to_id = to_id
        instance.sequence = int(sequence)
        instance.save(created_at=created_at)

    @classmethod
    def unlink(cls, from_id, to_id):
        assert from_id and to_id
        instance = cls()
        instance.from_id = from_id
        instance.to_id = to_id
        instance.delete()

    @classmethod
    def count(cls, from_id):
        sql = '''SELECT COUNT(1) AS counter FROM {table_name}
        WHERE `from_id`=%s'''.format(table_name=cls.table_name)

        with cls.get_sharding_db(from_id) as db:
            with db.get_connection().cursor() as cursor:
                cursor.execute(sql, (from_id, ))
                row = cursor.fetchone()
                if row and row.get('counter'):
                    return row.get('counter')
        return 0

    @classmethod
    def exists(cls, from_id, to_id):
        if None in (from_id, to_id): return False
        sql = '''SELECT COUNT(1) AS counter FROM {table_name}
        WHERE `from_id`=%s AND `to_id`=%s LIMIT 1
        '''.format(table_name=cls.table_name)
        with cls.get_connection() as cursor:
            cursor.execute(sql, (from_id, to_id, ))
            row = cursor.fetchone()
            if row and row.get('counter'):
                return row.get('counter') == 1
        return False

    @classmethod
    def multi_exists(cls, from_id, to_ids):
        assert isinstance(to_ids, list) or isinstance(to_ids, tuple)
        sql = '''SELECT `to_id` FROM {table_name}
        WHERE `from_id`=%s AND `to_id` IN %s
        '''.format(table_name=cls.table_name)
        with cls.get_connection() as cursor:
            cursor.execute(sql, (from_id, to_ids, ))
            rows = cursor.fetchall()
            return rows and [r.get('to_id') for r in rows] or []

    @classmethod
    def pagination(cls, from_id, offset=0, limit=20, desc=True):
        sorting = 'DESC'
        if not desc: sorting = 'ASC'

        sql = '''SELECT * FROM {table_name}
        WHERE `from_id`=%s
        ORDER BY `sequence` {sorting}, `created_at` {sorting}
        LIMIT %s, %s'''.format(table_name=cls.table_name, sorting=sorting)

        with cls.get_connection() as cursor:
            cursor.execute(sql, (from_id, offset, limit))
            return cursor.fetchall()

    @classmethod
    def objects(cls, obj_cls, from_id, offset=0, limit=20, desc=True):
        relations = cls.pagination(from_id, offset, limit, desc)
        if not relations: return []
        return [obj_cls.single(r.get('to_id')) for r in relations]

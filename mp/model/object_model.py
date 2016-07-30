# -*- coding: utf8 -*-

import datetime
import hashlib
import json
import types

from .id_model import IdModel


class ObjectModel(IdModel):

    DEFAULT_SUB_TYPE = 0
    DEFAULT_STATUS = 0

    def __init__(self, *args, **kwargs):
        super(ObjectModel, self).__init__(*args, **kwargs)
        self._parent_id = kwargs.get('parent_id', 0)
        self._uhash = kwargs.get('uhash', None)
        self._sub_type = kwargs.get('sub_type', self.DEFAULT_SUB_TYPE)
        self._status = kwargs.get('status', self.DEFAULT_STATUS)
        self._created_at = kwargs.get('created_at')
        self._updated_at = kwargs.get('updated_at')
        self._is_deleted = kwargs.get('is_deleted', 0) == 1
        row_data = kwargs.get('data')
        if row_data is not None:
            self._data = json.loads(row_data)
        else:
            self._data = dict()

    @classmethod
    def get_all_sub_types(cls):
        raise NotImplementedError()

    @classmethod
    def get_all_status(cls):
        return (ObjectModel.DEFAULT_STATUS, )

    def _get_parent_id(self):
        return self._parent_id
    def _set_parent_id(self, parent_id):
        self._parent_id = int(parent_id)
        return self
    parent_id = property(_get_parent_id, _set_parent_id)

    def _get_sub_type(self):
        return self._sub_type
    def _set_sub_type(self, sub_type):
        self._sub_type = int(sub_type)
        return self
    sub_type = property(_get_sub_type, _set_sub_type)

    def _get_status(self):
        return self._status
    def _set_status(self, status):
        self._status = int(status)
        return self
    status = property(_get_status, _set_status)

    def md5_uhash(self, dikt):
        '''Help method to generate a md5-based uhash, this is NOT a must
        '''
        assert isinstance(dikt, dict), 'Support dict-based uhash md5 only'
        joined = []
        [joined.extend(_tuple) for _tuple in sorted(dikt.items())]
        assert len(joined) > 0, 'Zero input to generate uhash md5'
        assert None not in joined, 'None is not permitted when generating uhash md5'
        return hashlib.md5(':'.join(map(str, joined))).hexdigest()

    @property
    def uhash(self):
        return self._uhash

    def get_uhash(self):
        return None

    def _get_created_at(self):
        return self._created_at
    def _set_created_at(self, created_at):
        self._created_at = created_at
        return self
    created_at = property(_get_created_at, _set_created_at)

    def _get_updated_at(self):
        return self._updated_at
    def _set_updated_at(self, updated_at):
        self._updated_at = updated_at
        return self
    updated_at = property(_get_updated_at, _set_updated_at)

    def _get_is_deleted(self):
        return self._is_deleted
    def _set_is_deleted(self, is_deleted):
        self._is_deleted = int(is_deleted)
        return self
    is_deleted = property(_get_is_deleted, _set_is_deleted)

    def get_data_field(self, key, default=None):
        return self._data.get(key, default)

    def set_data_field(self, key, value):
        self._data[key] = value
        return self

    def del_data_field(self, key):
        if key in self._data:
            del self._data[key]
        return self

    @property
    def data(self):
        return self._data

    def _sql_sub_types(self, cls, sub_types):
        if sub_types is None: return cls.get_all_sub_types()
        if type(sub_types) not in (types.ListType, types.TupleType):
            sub_types = (sub_types, )
        return sub_types

    def _sql_status(self, cls, status):
        if status is None: status = cls.get_all_status()
        if type(status) not in (types.ListType, types.TupleType):
            status = (status, )
        return status

    def save(self, created_at=None):
        if self.id is not None: return self.update()
        self.created_at = datetime.datetime.now()
        sql = '''INSERT INTO {table_name} (
            `parent_id`, `uhash`, `sub_type`, `status`, `data`, `created_at`, `is_deleted`
        ) VALUES(%s, %s, %s, %s, %s, %s, %s)
        '''.format(table_name=self.table_name)
        with self.get_connection() as cursor:
            cursor.execute(sql, (
                self.parent_id,
                self.get_uhash(),
                self.sub_type,
                self.status,
                json.dumps(self.data),
                self.created_at,
                self.is_deleted))
            self._id = cursor.lastrowid
        self.post_save()

    def post_save(self):
        pass

    def update(self):
        if self.id is None: return self.save()

        sql = '''UPDATE {table_name}
        SET `parent_id`=%s, `uhash`=%s, `sub_type`=%s, `status`=%s, `data`=%s, `is_deleted`=%s, `created_at`=%s
        WHERE `id`=%s'''.format(table_name=self.table_name)
        with self.get_connection() as cursor:
            cursor.execute(sql, (
                self.parent_id,
                self.get_uhash(),
                self.sub_type,
                self.status,
                json.dumps(self.data),
                self.is_deleted,
                self.created_at,
                self.id, ))
        self.post_update()
        return dict(_mc_key=(self.table_name, self.id))

    def post_update(self):
        pass

    def delete(self, hard_delete=False):
        if self.id is None: return

        soft_delete_sql = '''UPDATE {table_name}
        SET `is_deleted`=1
        WHERE `id`=%s'''.format(table_name=self.table_name)

        hard_delete_sql = '''DELETE FROM {table_name}
        WHERE `id`=%s'''.format(table_name=self.table_name)

        sql = hard_delete and hard_delete_sql or soft_delete_sql
        with self.get_connection() as cursor:
            cursor.execute(sql, (self.id, ))
        self.post_delete()
        return dict(_mc_key=(self.table_name, self.id))

    def post_delete(self):
        pass

    def parent(self, cls):
        if not self.parent_id: return None
        return cls.single(self.parent_id)

    def _sql_sub_types(self, cls, sub_types):
        if sub_types is None: return cls.get_all_sub_types()
        if type(sub_types) not in (types.ListType, types.TupleType):
            sub_types = (sub_types, )
        return sub_types

    def _sql_status(self, cls, status):
        if status is None: status = cls.get_all_status()
        if type(status) not in (types.ListType, types.TupleType):
            status = (status, )
        return status

    def children(self, cls, offset=0, limit=20,
                 sub_types=None,
                 status=None,
                 include_deleted=False,
                 id_only=False):
        if not self.id: return []

        selection = id_only and 'id' or '*'
        deletion = include_deleted and 'AND 1' or 'AND `is_deleted`=0'

        sql = '''SELECT {selection} FROM {table_name}
        WHERE `parent_id`=%s
        AND `sub_type` IN %s
        AND `status` IN %s
        {deletion}
        ORDER BY `created_at` DESC
        LIMIT %s, %s'''.format(
                selection=selection,
                deletion=deletion,
                table_name=cls.table_name)

        with self.get_connection() as cursor:
            cursor.execute(sql, (self.id,
                    self._sql_sub_types(cls, sub_types),
                    self._sql_status(cls, status),
                    offset,
                    limit, ))
            rows = cursor.fetchall()
            if id_only: return [r.get('id') for r in rows]
            else: return [cls.factory(row) for row in rows]

    def child_count(self, cls,
                sub_types=None,
                status=None,
                include_deleted=False):
        if not self.id: return 0

        deletion = include_deleted and 'AND 1' or 'AND `is_deleted`=0'
        sql = '''SELECT COUNT(1) AS counter FROM {table_name}
        WHERE `parent_id`=%s
        AND `sub_type` IN %s
        AND `status` IN %s
        {deletion}
        '''.format(
                deletion=deletion,
                table_name=cls.table_name)

        with self.get_connection() as cursor:
            cursor.execute(sql, (self.id,
                    self._sql_sub_types(cls, sub_types),
                    self._sql_status(cls, status), ))
            row = cursor.fetchone()
            return row and row.get('counter') or 0

    @classmethod
    def one_from_uhash(cls, sharding_id, uhash):
        if not uhash: return None

        sql = '''SELECT * FROM {table_name}
        WHERE `uhash`=%s
        LIMIT 1'''.format(table_name=cls.table_name)

        with cls.get_connection() as cursor:
            cursor.execute(sql, (uhash,))
            row = cursor.fetchone()
            return row and cls.factory(row) or None

    @classmethod
    def set_status(cls, parent_id, ids, new_status):
        sql = '''UPDATE {table_name}
        SET `status`=%s
        WHERE `parent_id`=%s
        AND `id` IN %s
        '''.format(table_name=cls.table_name)

        with cls.get_connection as cursor:
            cursor.execute(sql, (new_status, parent_id, ids, ))

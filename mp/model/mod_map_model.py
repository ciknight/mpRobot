# -*- coding: utf8 -*-

import types

from .id_model import IdModel


class ModMapModel(IdModel):

    table_name = 'mod_map'
    def __init__(self, *args, **kwargs):
        super(ModMapModel, self).__init__(*args, **kwargs)
        self._remaining = kwargs.get('remaing')
        self._from_network_type_id = kwargs.get('from_network_type_id')
        self._from_network_internal_id = kwargs.get('from_network_internal_id')
        self._to_network_type_id = kwargs.get('to_network_type_id')
        self._to_network_internal_id = kwargs.get('to_network_internal_id')

    def _get_remaining(self):
        return self._remaining
    def _set_remaining(self, remaining):
        if self._remaining is not None:
            raise ValueError('remaining is read-only once set')
        self._remaining = long(remaining)
        return self
    remaining = property(_get_remaining, _set_remaining)

    def _get_from_network_type_id(self):
        return self._from_network_type_id
    def _set_from_network_type_id(self, type_id):
        if self._from_network_type_id is not None:
            raise ValueError('from_network_type_id is read-only once set')
        self._from_network_type_id = long(type_id)
        return self
    from_network_type_id = property(_get_from_network_type_id, _set_from_network_type_id)

    def _get_from_network_internal_id(self):
        return self._from_network_internal_id
    def _set_from_network_internal_id(self, internal_id):
        if self._from_network_internal_id is not None:
            raise ValueError('from_network_internal_id is read-only once set')
        if type(internal_id) is types.UnicodeType:
            internal_id = internal_id.encode('utf-8')
        elif type(internal_id) is not types.StringType:
            internal_id = str(internal_id)
        self._from_network_internal_id = internal_id
        return self
    from_network_internal_id = property(
            _get_from_network_internal_id,
            _set_from_network_internal_id)

    def _get_to_network_type_id(self):
        return self._to_network_type_id
    def _set_to_network_type_id(self, type_id):
        self._to_network_type_id = long(type_id)
        return self
    to_network_type_id = property(_get_to_network_type_id, _set_to_network_type_id)

    def _get_to_network_internal_id(self):
        return self._to_network_internal_id
    def _set_to_network_internal_id(self, internal_id):
        self._to_network_internal_id = str(internal_id)
        return self
    to_network_internal_id = property(
            _get_to_network_internal_id,
            _set_to_network_internal_id)

    def save(self):
        if self.id is not None:
            return self.update()

        sql = '''INSERT INTO {table_name}
        (
            `from_network_type_id`, `from_network_internal_id`,
            `to_network_type_id`, `to_network_internal_id`
        ) VALUES (%s, %s, %s, %s)
        '''.format(table_name=self.table_name)

        with self.get_connection() as cursor:
            cursor.execute(sql, (
                    self.from_network_type_id,
                    self.from_network_internal_id,
                    self.to_network_type_id,
                    self.to_network_internal_id, ))
            self._id = cursor.lastrowid

    def update(self):
        if self.id is None:
            return self.save()

        sql = '''UPDATE {table_name} SET
        `to_network_type_id`=%s,
        `to_network_internal_id`=%s
        WHERE `id`=%s'''.format(table_name=self.table_name)
        with self.get_connection() as cursor:
            cursor.execute(sql, (
                self.to_network_type_id,
                self.to_network_internal_id,
                self.id, ))

    def delete(self):
        if self.id is not None:
            sql = 'DELETE FROM {table_name} WHERE `id`=%s'.format(
                    table_name=self.table_name)
            with self.get_connection() as cursor:
                cursor.execute(sql, (self.id, ))

    @classmethod
    def exists(cls, from_network_type_id, from_network_internal_id,
               to_network_type_id):
        return cls.one_by_from_network(from_network_type_id, from_network_internal_id,
                                       to_network_type_id) is not None

    @classmethod
    def link(cls, from_network_type_id, from_network_internal_id,
             to_network_type_id, to_network_internal_id):
        instance = cls()
        instance.from_network_type_id = from_network_type_id
        instance.from_network_internal_id = from_network_internal_id
        instance.to_network_type_id = to_network_type_id
        instance.to_network_internal_id = to_network_internal_id
        instance.save()

    @classmethod
    def unlink(cls, from_network_type_id, from_network_internal_id, to_network_type_id):
        instance = cls.one_by_from_network(from_network_type_id, from_network_internal_id,
                                           to_network_type_id)
        if instance is not None:
            instance.delete()

    @classmethod
    def one_by_from_network(cls, from_type, from_id, to_type):
        sql = '''SELECT * FROM {table_name}
        WHERE `from_network_type_id`=%s
        AND `from_network_internal_id`=%s
        AND `to_network_type_id`=%s
        '''.format(table_name=cls.table_name)

        if type(from_id) is types.UnicodeType:
            from_id = from_id.encode('utf-8')
        elif type(from_id) is not types.StringType:
            from_id = str(from_id)
        with cls.get_connection() as cursor:
            cursor.execute(sql, (from_type, from_id, to_type, ))
            return cls.factory(cursor.fetchone())

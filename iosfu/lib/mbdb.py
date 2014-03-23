from __future__ import with_statement


class FieldType(object):
    _type = None
    bits = None

    def __init__(self, bits=8, *args, **kwargs):
        self.bits = bits

    def read_property(self, handler):
        return handler.read(int(self.bits/8))


class Integer(FieldType):
    _type = int
    bits = 8

    def to_int(self, bytes_or_buffer):
        if hasattr(int, 'from_bytes'):  # Python3
            result = int.from_bytes(bytes_or_buffer, 'big')
        else:  # < Python 3
            result = int(bytes_or_buffer.encode('hex'), 16)

        return result

    def read_property(self, *args, **kwargs):
        prop = super(Integer, self).read_property(*args, **kwargs)
        result = self.to_int(prop)
        return result


class String(FieldType):
    _type = str
    bits = None

    def read_property(self, handler):
        length = Integer(16).read_property(handler)
        # if 0x0000 or 0xFFFF, dont read cause its empty!
        if length != 0 and length != 65535:
            self.bits = length*8
            return super(String, self).read_property(handler)


class Entry(object):
    _fields = ()

    def read(self, handler):
        for field in self._fields:
            try:
                field_type = field[1](field[2])
            except IndexError:
                field_type = field[1]()

            print(field[0])

            field_value = field_type.read_property(handler)

            setattr(self, field[0], field_value)


class Property(Entry):
    key = None
    value = None

    _fields = (
        ('key', String, ),
        ('value', String, ),
    )


class Record(Entry):
    domain = None
    path = None
    target = None
    hash = None
    encryption_key = None
    mode = None
    inode_number = None
    user_id = None
    group_id = None
    last_modified = None
    last_accesed = None
    created = None
    filesize = None
    flag = None
    properties_number = None
    properties = []

    _fields = (
        ('domain', String, ),
        ('path', String, ),
        ('target', String, ),
        ('hash', String, ),
        ('encryption_key', String, ),
        ('mode', Integer, 16, ),
        ('inode_number', Integer, 64, ),
        ('user_id', Integer, 32, ),
        ('group_id', Integer, 32, ),
        ('last_modified', Integer, 32, ),
        ('last_accesed', Integer, 32, ),
        ('created', Integer, 32, ),
        ('filesize', Integer, 64, ),
        ('flag', Integer, 8, ),
        ('properties_number', Integer, 8, ),
        # ('properties', None, ),
    )

    def read(self, handler):
        super(Record, self).read(handler)
        self.read_properties(handler)

    def read_properties(self, handler):
        if self.properties_number > 0:
            for prop in range(self.properties_number):
                record_property = Property()
                record_property.read(handler)

                self.properties.append(record_property)


class MBDB(object):
    _handler = None

    header = None
    records = []

    def __init__(self, path):
        self._handler = open(path, 'rb')
        print(dir(self._handler))
        self.read_header()

    def read_header(self):
        self.header = self._handler.read(6)

    def read_record(self):
        record = Record()
        try:
            record.read(self._handler)
        except ValueError:
            record = False

        return record

    def read(self):
        while self._handler:
            record = self.read_record()

            if record:
                self.records.append(record)
                yield record
            else:
                break

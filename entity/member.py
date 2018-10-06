
from old_jvm1.utils.enum1 import *



class Member:
    def __init__(self, constants):
        self.access_flag = None
        self.name_index = None
        self.desc_index = None
        self.attributes = None
        self.constants = constants

    def read_info(self, reader):
        self.access_flag = reader.read_uint(2)
        self.name_index = reader.read_uint(2)
        self.desc_index = reader.read_uint(2)
        self.attributes = reader.read_attributes(self.constants)

    def get_name(self):
        return self.constants.get_constant(self.name_index)

    def get_desc(self):
        return self.constants.get_constant(self.desc_index)

    def get_access_flag(self):
        return self.access_flag

    def get_code_attribute(self):
        for a in self.attributes:
            if a.__class__.__name__ == 'CodeAttribute':
                return a
        return None

    def get_constantvalue_attr(self):
        for a in self.attributes:
            if a.__class__.__name__ == 'ConstantValueAttribute':
                return a
        return None

    def get_constant_value(self):
        for a in self.attributes:
            if a.__class__.__name__ == 'ConstantValueAttribute':
                v = self.constants.get_constant(a.index)
                return v
        return None

class RuntimeMember:
    def __init__(self, member, klass=None):
        self.klass = klass
        self.copy_memberInfo(member)

    def set_klass(self, klass):
        self.klass = klass

    def copy_memberInfo(self, member):
        self.access_flag = member.get_access_flag()
        self.name = member.get_name()
        self.desc = member.get_desc()

    def is_static(self):
        return self.access_flag & AccessType.STATIC.value

    def is_final(self):
        return self.access_flag & AccessType.FINAL.value

    def is_native(self):
        return self.access_flag & AccessType.NATIVE.value

class Field(RuntimeMember):
    def __init__(self, field, klass):
        super(Field, self).__init__(field, klass)
        self.copy_attributes(field)
        self.id = None

    def copy_attributes(self, field):
        attr = field.get_constantvalue_attr()
        if attr:
            self.constant_value = field.get_constant_value()
        else:
            self.constant_value = None

    def is_long_or_double(self):
        return self.desc == 'J' or self.desc == 'D'

    def is_big_field(self):
        return self.desc == 'J' or self.desc == 'D'

    def get_constant_value(self):
        return self.constant_value


class Method(RuntimeMember):
    def __init__(self, method, klass):
        super(Method, self).__init__(method, klass)
        self.copy_attributes(method)
        self.arguments_length = self.calculate_arguments_length()

        if self.is_native():
            self.inject_code_attr(method)

    def copy_attributes(self, method):
        attr = method.get_code_attribute()
        if attr:
            self.max_stack = attr.get_max_stack()
            self.max_locals = attr.get_max_locals()
            self.bytecode = attr.get_bytecode()
        # else:
        #     self.max_stack = 0
        #     self.max_locals = 0
        #     self.bytecode = ''

    def get_constants(self):
        return self.klass.get_constants()

    def parse_desc(self, desc):
        parser = DescParser(desc)
        parser.parse()
        return parser

    def get_arguments_length(self):
        return self.arguments_length

    def calculate_arguments_length(self):
        parser = self.parse_desc(self.desc)
        params = parser.params
        count = 0
        for p in params:
            count += 1
            if p == 'J' or p == 'D':
                count += 1

        # tochange
        if not self.is_static():
            count += 1
        return count

    def get_return_type(self):
        parser = self.parse_desc(self.desc)
        return parser.return_type

    def inject_code_attr(self, method):
        self.max_stack = 4
        self.max_locals = self.get_arguments_length()

        t = self.get_return_type()
        if t == 'V':
            self.bytecode = b'\xfe\xb1'
        elif t == 'D':
            self.bytecode = b'\xfe\xaf'
        elif t == 'F':
            self.bytecode = b'\xfe\xae'
        elif t == 'J':
            self.bytecode = b'\xfe\xad'
        elif t == 'L':
            self.bytecode = b'\xfe\xb0'
        else:
            self.bytecode = b'\xfe\xac'

    def get_class_name(self):
        if self.klass:
            return self.klass.name
        return None

class DescParser:
    def __init__(self, desc):
        self.index = 0
        self.desc = desc
        self.params = None
        self.return_type = None

    def parse(self):
        if self.next() != '(':
            raise Exception('not (  desc:', self.desc)
        self.params = self.parse_param()
        if self.next() != ')':
            raise Exception('not )  desc:', self.desc)
        self.return_type = self.next()

    def parse_param(self):
        params = []
        while True:
            p = self.parse_field()
            if p:
                params.append(p)
            else:
                self.back()
                return params
        raise Exception('should not arrive')

    def parse_field(self):
        cur = self.next()
        if cur in ['B', 'C', 'D', 'F', 'I', 'J', 'S', 'Z']:
            p = cur
        elif cur == 'L':
            p = self.parse_object_type()
        elif cur == '[':
            p = self.parse_array_type()
        else:
            p = None
        return p

    def parse_object_type(self):
        desc = ''
        cur = self.next()
        while cur != ';':
            desc += cur
            cur = self.next()
        return desc

    def parse_array_type(self):
        desc = '[' + self.parse_field()
        return desc

    def next(self):
        cur = self.cur()
        self.index += 1
        return cur

    def back(self):
        self.index -= 1

    def cur(self):
        return self.desc[self.index]

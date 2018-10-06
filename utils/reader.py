import os.path
from zipfile import *

from old_jvm1.entity.attribute import *
from old_jvm1.entity.constant import *
from old_jvm1.entity.constant_pool import *
from old_jvm1.entity.member import *
from old_jvm1.utils.config import *
from old_jvm1.utils.factory import constant_factory, attribute_factory


class BaseReader:
    def __init__(self, bytes):
        self.bytes = bytes
        self.index = 0

    def read_bytes(self, count):
        bytes = b''
        for i in range(count):
            byte = self.read_byte()
            bytes += byte
        return bytes

    def read_byte(self):
        b = self.bytes[self.index:self.index+1]
        self.index += 1
        return b

    def read_int(self, byte_count):
        bytes = self.read_bytes(byte_count)
        i = int.from_bytes(bytes, byteorder='big', signed=True)
        return i

    def read_uint(self, byte_count):
        bytes = self.read_bytes(byte_count)
        i = int.from_bytes(bytes, byteorder='big')
        return i

    def read_ints(self, byte_count):
        n = self.read_int(2)
        integers = []
        for i in range(n):
            integer = self.read_int(byte_count)
            integers.append(integer)
        return integers

class Reader(BaseReader):
    def read_constants(self):
        unvalid = UnvalidConstant()
        constants = [unvalid]
        capacity = self.read_uint(2)
        i = 1
        while i < capacity:
            const = self.read_constant()
            const.set_constantpool(constants)
            constants.append(const)
            if const.is_type('LongConstant') or const.is_type('DoubleConstant'):
                c = UnvalidConstant()
                constants.append(unvalid)
                i += 1
            i += 1
        cp = ConstantPool(constants)
        rtcp = cp.resolve()
        return rtcp

    def read_constant(self):
        tag = self.read_uint(1)
        const = self.read_constant_for_tag(tag)
        return const

    def read_constant_for_tag(self, tag):
        contructor = constant_factory[tag]
        const = contructor()
        const.read_info(self)
        return const

    def read_attributes(self, constant_pool):
        attrs = []
        count = self.read_int(2)
        for i in range(count):
            attr = self.read_attribute(constant_pool)
            attrs.append(attr)
        return attrs

    def read_attribute(self, constant_pool):
        index = self.read_int(2)
        attr_name = constant_pool.get_constant(index)
        attr = self.get_attribute(attr_name, constant_pool)
        return attr

    def get_attribute(self, attribute_name, constant_pool):
        if attribute_name not in attribute_factory:
            attr = UnparseAttribute()
        else:
            contructor = attribute_factory[attribute_name]
            attr = contructor()
        self.read_info(attr, constant_pool)
        return attr

    def read_info(self, attribute, constant_pool):
        attr = attribute
        if attr.is_type('CodeAttribute'):
            attr.read_info(self, constant_pool)
        else:
            attr.read_info(self)

    def read_members(self, constant_pool):
        count = self.read_uint(2)
        members = []
        for i in range(count):
            m = self.read_member(constant_pool)
            members.append(m)
        return members

    def read_member(self, constant_pool):
        m = Member(constant_pool)
        m.read_info(self)
        return m

class CodeReader(BaseReader):
    def set_next_pc(self, pc):
        self.index = pc

    def get_next_pc(self):
        return self.index

    def get_opcode(self):
        return self.read_uint(1)

class FileReader:
    def read(self, qualified_name):
        filename = qualified_name + '.class'
        data = self.find_bootstrap(filename)
        if not data:
            data = self.find_extern(filename)
        if not data:
            data = self.find_user(filename)
        return data

    def find_bootstrap(self, filename):
        return self.read_file(bootstrap_path, filename)

    def find_extern(self, filename):
        return self.read_file(extension_path, filename)

    def read_file(self, dirpath, filename):
        filepaths = self.get_jarfiles(dirpath)
        for path in filepaths:
            data = self.read_from_jar(path, filename)
            if data:
                return data

    def read_from_jar(self, jarpath, filename):
        with ZipFile(jarpath) as myzip:
            for name in myzip.namelist():
                if name == filename:
                    with myzip.open(name) as fin:
                        return fin.read()

    def get_jarfiles(self, dir):
        filenames = os.listdir(dir)
        target = []
        postfix = '.jar'
        for name in filenames:
            if name.endswith(postfix):
                p = os.path.join(dir, name)
                target.append(p)
        return target

    def find_user(self, filename):
        path = os.path.join(user_path, filename)
        with open(path, 'rb') as f:
            return f.read()

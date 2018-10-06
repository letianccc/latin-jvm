
from old_jvm1.utils.reader import *


class ClassFile:
    def __init__(self, data):
        reader = Reader(data)
        self.magic = reader.read_uint(4)
        self.minor_version = reader.read_uint(2)
        self.major_version = reader.read_uint(2)
        self.constants = reader.read_constants()
        self.access_flag = reader.read_uint(2)
        self.class_index = reader.read_uint(2)
        self.superclass_index = reader.read_uint(2)
        self.interfaces = reader.read_ints(2)
        self.fields = reader.read_members(self.constants)
        self.methods = reader.read_members(self.constants)
        self.attributes = reader.read_attributes(self.constants)

    def get_fields(self, klass):
        fields = []
        for f in self.fields:
            new_field = Field(f, klass)
            fields.append(new_field)
        return fields

    def get_methods(self, klass):
        methods = []
        for m in self.methods:
            new_method = Method(m, klass)
            methods.append(new_method)
        return methods

    def get_constant_pool(self, klass):
        self.constants.set_klass(klass)
        return self.constants

    def get_superclass_name(self):
        class_constant = self.constants.get_constant(self.superclass_index)
        if class_constant is None:
            return None
        return class_constant.get_class_name()

    def get_class_name(self):
        class_constant = self.constants.get_constant(self.class_index)
        return class_constant.get_class_name()

    def get_interface_names(self):
        names = []
        for index in self.interfaces:
            name = self.constants.get_constant(index)
            names.append(name)
        return names

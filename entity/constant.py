
import struct





class Constant():
    def is_type(self, constant_type):
        name = self.__class__.__name__
        return name == constant_type

    def get_type(self):
        return self.__class__.__name__

    def set_constantpool(self, constants):
        self.constants = constants

class UnvalidConstant(Constant):
    def get_value(self, constant_pool=None):
        return None

class Utf8Constant(Constant):
    def __init__(self):
        self.value = None

    def read_info(self, reader):
        length = reader.read_int(2)
        if length == 0:
            return None
        byte = reader.read_bytes(length)
        self.value = byte.decode("utf-8")

    def get_value(self):
        return self.value

class StringConstant(Constant):
    def __init__(self):
        self.index = None
        self.constants = None

    def read_info(self, reader):
        self.index = reader.read_int(2)

    def get_value(self):
        return self.constants[self.index].get_value()

class IntConstant(Constant):
    def __init__(self):
        self.value = None

    def read_info(self, reader):
        const = reader.read_int(4)
        self.value = const

    def get_value(self):
        return self.value


class FloatConstant(Constant):
    def __init__(self):
        self.value = None

    def read_info(self, reader):
        byte = reader.read_bytes(4)
        (const, ) = struct.unpack('>f', byte)
        self.value = const

    def get_value(self):
        return self.value

class LongConstant(Constant):
    def __init__(self):
        self.value = None

    def read_info(self, reader):
        byte = reader.read_bytes(8)
        (const, ) = struct.unpack('>q', byte)
        self.value = const

    def get_value(self):
        return self.value

class DoubleConstant(Constant):
    def __init__(self):
        self.value = None

    def read_info(self, reader):
        byte = reader.read_bytes(8)
        (const, ) = struct.unpack('>d', byte)
        self.value = const

    def get_value(self):
        return self.value

class ClassConstant(Constant):
    def __init__(self):
        self.index = None
        self.constants = None

    def read_info(self, reader):
        self.index = reader.read_int(2)

    def get_value(self):
        return self.constants[self.index].get_value()

    def get_name(self):
        return self.constants[self.index].get_value()



class RefConstant(Constant):
    def __init__(self):
        self.class_index = None
        self.name_and_type_index = None
        self.constants = None

    def read_info(self, reader):
        self.class_index = reader.read_int(2)
        self.name_and_type_index = reader.read_int(2)

    def get_class_name(self):
        return self.constants[self.class_index].get_value()

    def get_name(self):
        const = self.constants[self.name_and_type_index]
        return const.get_name()

    def get_desc(self):
        const = self.constants[self.name_and_type_index]
        return const.get_desc()

class FieldRefConstant(RefConstant):
    pass

class MethodRefConstant(RefConstant):
    pass

class InterfaceMethodRefConstant(RefConstant):
    pass


class NameAndTypeConstant(Constant):
    def __init__(self):
        self.name_index = None
        self.descriptor_index = None
        self.constants = None

    def read_info(self, reader):
        self.name_index = reader.read_int(2)
        self.descriptor_index = reader.read_int(2)

    def get_name(self):
        return self.constants[self.name_index].get_value()

    def get_desc(self):
        return self.constants[self.descriptor_index].get_value()


from old_jvm1.entity.ref import *

class ConstantPool:
    def __init__(self, constants):
        self.constants = constants
        self.resolve_methods = None

    def get_constant(self, index):
        return self.constants[index]

    def get_capacity(self):
        return len(self.constants)

    def resolve(self):
        target = []
        self.set_resolve_methods()
        for const in self.constants:
            v = self.resolve_constant_value(const)
            target.append(v)
        cp = RuntimeConstantPool(target)
        return cp

    def resolve_constant_value(self, constant):
        kind = constant.get_type()
        method = self.resolve_methods[kind]
        value = method(constant)
        return value

    def set_resolve_methods(self):
        self.resolve_methods = self.get_resolve_methods()

    def get_resolve_methods(self):
        methods = {
            'ClassConstant': self.new_classref,
            'FieldRefConstant': self.new_fieldref,
            'MethodRefConstant': self.new_methodref,
            'InterfaceMethodRefConstant': self.new_interfacemethodref,
            'StringConstant': self.resolve_string,
            'UnvalidConstant': self.get_literal,
            'IntConstant': self.get_literal,
            'FloatConstant': self.get_literal,
            'LongConstant': self.get_literal,
            'DoubleConstant': self.get_literal,
            'Utf8Constant': self.get_literal,
            'NameAndTypeConstant': self.not_resolve,
        }
        return methods

    def get_literal(self, constant):
        return constant.get_value()

    def resolve_string(self, string_constant):
        return string_constant.get_value()

    def not_resolve(self, constant):
        return None

    def new_classref(self, class_const):
        class_name = class_const.get_value()
        ref = ClassRef(class_name)
        return ref

    def new_methodref(self, methodConstant):
        c = methodConstant
        class_name = c.get_class_name()
        method_name = c.get_name()
        desc = c.get_desc()
        ref = MethodRef(class_name, method_name, desc)
        return ref

    def new_fieldref(self, fieldConstant):
        c = fieldConstant
        class_name = c.get_class_name()
        field_name = c.get_name()
        desc = c.get_desc()
        ref = FieldRef(class_name, field_name, desc)
        return ref

    def new_interfacemethodref(self, interfaceMethodConstant):
        c = interfaceMethodConstant
        class_name = c.get_class_name()
        method_name = c.get_name()
        desc = c.get_desc()
        ref = InterfaceMethodRef(class_name, method_name, desc)
        return ref


class RuntimeConstantPool:
    def __init__(self, constants):
        self.constants = constants
        self.cp = constants

    def get_constant(self, index):
        return self.constants[index]

    def get_capacity(self):
        return len(self.constants)

    def set_klass(self, klass):
        for c in self.constants:
            if isinstance(c, SymbolRef):
                c.referenced_klass = klass

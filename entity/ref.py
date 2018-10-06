

class SymbolRef:
    def __init__(self, class_name):
        self.class_name = class_name
        self.klass = None
        self.referenced_klass = None

    def get_type(self):
        return self.__class__.__name__

    def resolve_class(self):
        from old_jvm1.core.class_loader import Loader
        if not self.klass:
            self.klass = self.referenced_klass.loader.load(self.class_name)
            #TODO access_flag 可能有错  field、method 和klass 访问控制可能不同
            self.access_flag = self.klass.access_flag

        return self.klass

    def get_class_name(self):
        return self.class_name

class ClassRef(SymbolRef):
    def resolve(self):
        return self.resolve_class()

class MemberRef(SymbolRef):
    def __init__(self, class_name, member_name, desc):
        super(MemberRef, self).__init__(class_name)
        self.name = member_name
        self.desc = desc

class FieldRef(MemberRef):
    def __init__(self, class_name, field_name, desc):
        super(FieldRef, self).__init__(class_name, field_name, desc)
        self.field = None

    def resolve_field(self):
        if not self.field:
            self.klass = self.resolve_class()
            field = self.klass.find_field(self.name, self.desc)
            if not field:
                raise Exception('no such field in class')
            # if not field.is_accessable(self.cp.struct):
            #     raise Exception('no permit')
            self.field = field
        return self.field

    def is_accessable(self, struct):
        pass

class MethodRef(MemberRef):
    def __init__(self, class_name, method_name, desc):
        super(MethodRef, self).__init__(class_name, method_name, desc)
        self.method = None

    def resolve(self):
        if not self.method:
            self.klass = self.resolve_class()
            method = self.klass.find_method(self.name, self.desc)
            if not method:
                raise Exception('no such method in class')
            # if not method.is_accessable(self.cp.struct):
            #     raise Exception('no permit')
            self.method = method
        return self.method


class InterfaceMethodRef(SymbolRef):
    def __init__(self, class_name, name, desc):
        super(InterfaceMethodRef, self).__init__(class_name)
        self.name = name
        self.desc = desc

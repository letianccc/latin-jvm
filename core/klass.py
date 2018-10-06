from old_jvm1.entity.object import Object
from old_jvm1.utils.classname_util import get_desc, get_classname

class Klass:
    def __init__(self, classfile=None, loader=None):
        if classfile:
            cf = classfile
            self.access_flag = cf.access_flag
            self.name = cf.get_class_name()
            self.superclass_name = cf.get_superclass_name()
            self.interfaces = cf.get_interface_names()
            self.fields = cf.get_fields(self)
            self.methods = cf.get_methods(self)
            self.constant_pool = cf.get_constant_pool(self)
        self.n_instance_field = 0
        self.n_static_field = 0
        self.loader = loader
        self.init_start = False
        self.static_field_values = None
        self.class_klass = None
        self.superclass = None

    def init(self):
        self.init_start = True

    def get_constant_value(self, constant):
        t = constant.__class__.__name__

    def new_object(self, field_count=None):
        if not field_count:
            field_count = self.n_instance_field
        o = Object(self, field_count)
        return o

    def get_field_count(self):
        target = len(self.fields)
        if self.superclass:
            target += self.superclass.get_field_count()
        return target


    def new_array(self, size):
        if not self.is_array():
            raise Exception('not array')
        return Object(self, size)

    def load(self, classname):
        return self.loader.load(classname)

    def is_array(self):
        return self.name[0] == '['

    def get_main_method(self):
        for m in self.methods:
            if m.name == 'main' and m.desc == '([Ljava/lang/String;)V':
                return m
        return None

    def find_field(self, name, desc):
        for f in self.fields:
            if f.name == name and f.desc == desc:
                return f
        if self.superclass:
            return self.superclass.find_field(name, desc)
        return None

    def find_method(self, name, desc):
        for m in self.methods:
            if m.name == name and m.desc == desc:
                return m
        if self.superclass:
            m = self.superclass.find_method(name, desc)
            return m
        return None

    def get_clinit_method(self):
        return self.get_static_method('<clinit>', '()V')

    def get_static_method(self, name, desc):
        for m in self.methods:
            if m.is_static():
                if m.name == name and m.desc == desc:
                    return m
        return None

    def get_static_field(self, field_id):
        return self.static_field_values[field_id]

    def set_static_field(self, field_id, value):
        self.static_field_values[field_id] = value

    def is_interface(self):
        pass

    def get_instance_field(self, name, desc):
        cs = self
        while cs:
            for f in cs.fields:
                if f.name == name and f.desc == desc:
                    return f
            cs = self.superclass

    # def get_array_class(self):
    #     from old_jvm1.core.class_loader import Loader
    #     name = self.get_array_name()
    #     return Loader.load(name)

    # def get_array_name(self):
    #     return '[' + get_desc(self.name)

    # def get_element_klass(self):
    #     n = self.get_element_klassname()
    #     return self.referenced_klass.load(n)

    # def get_element_klassname(self):
    #     container_classname = self.name
    #     if container_classname[0] != '[':
    #         raise Exception('invalid classname: ', container_classname)
    #     element_desc = container_classname[1:]
    #     return get_classname(element_desc)

    def get_constants(self):
        return self.constant_pool

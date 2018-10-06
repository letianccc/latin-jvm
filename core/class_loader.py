from old_jvm1.core.classfile import *
from old_jvm1.core.klass import *
from old_jvm1.utils.classname_util import primitive
from old_jvm1.utils.reader import FileReader

initial_value = {
    'B': 0,
    'C': 0x0000,
    'D': 0.0,
    'F': 0.0,
    'I': 0,
    'J': 0,
    'S': 0,
    'Z': 0,
}

class Loader:
    def __init__(self):
        self.class_list = dict()
        self.reader = FileReader()

        self.load_basic_class()
        self.load_primitive_class()

    def load_basic_class(self):
        name = 'java/lang/Class'
        self.load(name)
        for klass in self.class_list.values():
            if not klass.class_klass:
                self.set_class_klass(klass)

    def load_primitive_class(self):
        for classname in primitive.values():
            klass = Klass()
            klass.access_flag = AccessType.PUBLIC
            klass.name = classname
            klass.init_start = True
            self.set_class_klass(klass)
            self.class_list[classname] = klass

    def load(self, classname):
        if classname in self.class_list:
            return self.class_list[classname]
        if classname[0] == '[':
            klass = self.load_array_class(classname)
        else:
            klass = self.load_not_array_class(classname)
        self.class_list[classname] = klass
        self.set_class_klass(klass)
        return klass

    def load_array_class(self, classname):
        klass = Klass(loader=self)
        klass.access_flag = AccessType.PUBLIC
        klass.name = classname
        klass.superclass = self.load('java/lang/Object')
        klass.init_start = True
        klass.methods = []
        return klass

    def load_not_array_class(self, classname):
        klass = self.define_class(classname)
        self.link(klass)
        return klass

    def set_class_klass(self, klass):
        name = 'java/lang/Class'
        if name in self.class_list:
            class_klass = self.class_list[name]
            class_object = class_klass.new_object()
            class_object.extra = klass
            klass.class_klass = class_object

    def define_class(self, classname):
        cf = self.get_classfile(classname)
        klass = self.get_klass(cf)
        self.load_superclass(klass)
        return klass

    def link(self, klass):
        self.prepare(klass)

    def prepare(self, klass):
        self.set_instance_field_id(klass)
        self.set_static_field_id(klass)
        self.init_static_field(klass)

    def set_instance_field_id(self, klass):
        id = 0
        if klass.superclass:
            id = klass.superclass.n_instance_field
        for f in klass.fields:
            if not f.is_static():
                f.id = id
                id += 1
                if f.is_big_field():
                    id += 1
        klass.n_instance_field = id

    def set_static_field_id(self, klass):
        id = 0
        for f in klass.fields:
            if f.is_static():
                f.id = id
                id += 1
                if f.is_big_field():
                    id += 1
        klass.n_static_field = id

    def init_static_field(self, klass):
        klass.static_field_values = [None] * klass.n_static_field
        for f in klass.fields:
            if f.is_static():
                v = self.get_initial_value(f)
                klass.set_static_field(f.id, v)

    def get_initial_value(self, static_field):
        from old_jvm1.utils.jstring import get_jstring
        f = static_field
        if f.is_final():
            v = f.get_constant_value()
            if v:
                if f.desc == 'Ljava/lang/String;':
                    v = get_jstring(v, self)
        else:
            v = initial_value.get(f.desc, None)
        return v

    def get_classfile(self, classname):
        bytes = self.reader.read(classname)
        if not bytes:
            raise Exception('get classfile fail, classname: ', classname)
        cf = ClassFile(bytes)
        return cf

    def get_klass(self, classfile):
        from old_jvm1.core.klass import Klass
        c = Klass(classfile, self)
        return c

    def load_superclass(self, klass):
        if klass.name != 'java/lang/Object':
            klass.superclass = self.load(klass.superclass_name)

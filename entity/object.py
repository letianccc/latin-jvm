
#TODO 分为引用对象和基本对象

class Object:
    def __init__(self, klass, field_count=None):
        # log('field ', field_count)
        self.klass = klass
        if field_count:
            self.fields = [None] * field_count
        self.field_count = field_count
        self.extra = None

    def set_field(self, index, value):
        self.fields[index] = value

    def get_field(self, index):
        return self.fields[index]

    def get_array_length(self):
        return len(self.fields)

    def set_ref_var(self, name, desc, ref):
        f = self.klass.get_instance_field(name, desc)
        pos = f.id
        self.set_field(pos, ref)

    def get_ref_var(self, name, desc):
        f = self.klass.get_instance_field(name, desc)
        pos = f.id
        return self.get_field(pos)

    def is_instance_of(self, klass):
        # todo  未考虑接口 子类
        return self.klass == klass

    def get_value(self):
        char_array = self.get_ref_var('value', '[C')
        return char_array.fields.decode('utf16')

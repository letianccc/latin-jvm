
from .instruction import Instruction, Initializer
from old_jvm1.utils.classname_util import get_desc, get_classname, array_type_to_classname


class BaseNew(Instruction):
    def execute(self, frame):
        klass = self.get_klass(frame)
        o = self.new_object(frame, klass)
        frame.push(o)

class New(BaseNew):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def get_klass(self, frame):
        cp = frame.method.get_constants()
        class_ref = cp.get_constant(self.index)
        klass = class_ref.resolve()
        if not klass.init_start:
            initializer = Initializer()
            initializer.init(frame.thread, klass)
        return klass

    def new_object(self, frame, klass):
        o = klass.new_object()
        return o

class SingleDimension(BaseNew):
    def get_array_size(self, frame):
        array_size = frame.pop()
        if array_size < 0:
            raise Exception('array_size < 0')
        return array_size

    def new_object(self, frame, array_class):
        array_size = self.get_array_size(frame)
        o = array_class.new_object(array_size)
        return o

class NewArray(SingleDimension):
    def read_operand(self, reader):
        self.array_type = reader.read_uint(1)

    def get_klass(self, frame):
        referenced_klass = frame.method.klass
        classname = array_type_to_classname[self.array_type]
        klass = referenced_klass.load(classname)
        return klass

class ANewArray(SingleDimension):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def get_klass(self, frame):
        referenced_klass = frame.method.klass
        name = self.get_classname(frame)
        klass = referenced_klass.load(name)
        return klass

    def get_classname(self, frame):
        cp = frame.method.get_constants()
        classref = cp.get_constant(self.index)
        name = '[' + get_desc(classref.class_name)
        return name

class MultiANewArray(BaseNew):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)
        self.dimension = reader.read_uint(1)

    def get_klass(self, frame):
        self.referenced_klass = frame.method.klass
        cp = frame.method.get_constants()
        classref = cp.get_constant(self.index)
        klass = classref.resolve()
        return klass

    def new_object(self, frame, array_class):
        self.array_sizes = self.get_array_sizes(frame)
        array = self.new_multiarray(array_class, 0)
        return array

    def new_multiarray(self, array_klass, dimension):
        size = self.array_sizes[dimension]
        array = array_klass.new_object(size)
        dimension += 1
        have_subarray = dimension < self.dimension
        if have_subarray:
            self.set_element(array, dimension)
        return array

    def set_element(self, container_object, dimension):
        klass = self.get_element_klass(container_object)
        array_size = container_object.field_count
        for i in range(array_size):
            element = self.new_multiarray(klass, dimension)
            container_object.set_field(i, element)

    def get_element_klass(self, container_object):
        name = self.get_element_classname(container_object.klass)
        klass = self.referenced_klass.load(name)
        return klass

    def get_element_classname(self, container_klass):
        container = container_klass.name
        if container[0] != '[':
            raise Exception('invalid classname: ', container)
        element_desc = container[1:]
        element = get_classname(element_desc)
        return element

    def get_array_sizes(self, frame):
        array_sizes = []
        for i in range(self.dimension):
            c = frame.pop()
            if c < 0:
                raise Exception('count < 0')
            array_sizes.insert(0, c)
        return array_sizes

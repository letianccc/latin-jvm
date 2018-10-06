
from .instruction import Instruction
from old_jvm1.utils.jstring import *


class IConst(Instruction):
    def __init__(self, const):
        self.const = const

    def execute(self, frame):
        frame.push(self.const)

class IConst2(Instruction):
    def __init__(self, const):
        self.const = const

    def execute(self, frame):
        frame.push2(self.const)

class ILoad(Instruction):
    def __init__(self, index):
        self.index = index

    def execute(self, frame):
        frame.load(self.index)

class ILoad2(Instruction):
    def __init__(self, index):
        self.index = index

    def execute(self, frame):
        frame.load2(self.index)

class Load(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(1)

    def execute(self, frame):
        frame.load(self.index)

class Load2(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(1)

    def execute(self, frame):
        frame.load2(self.index)

class BaseArrayLoad(Instruction):
    def execute(self, frame):
        index = frame.pop()
        array = frame.pop()
        e = array.get_field(index)
        self.push(frame, e)

class ArrayLoad(BaseArrayLoad):
    def push(self, frame, element):
        frame.push(element)

class ArrayLoad2(BaseArrayLoad):
    def push(self, frame, element):
        frame.push2(element)

class BaseLdc(Instruction):
    def execute(self, frame):
        const = self.get_constant(frame)
        target = self.convert(frame, const)
        self.push(frame, target)

    def get_constant(self, frame):
        cp = frame.method.get_constants()
        const = cp.get_constant(self.index)
        return const

    def convert(self, frame, constant):
        t = constant.__class__.__name__
        if t == 'ClassRef':
            target = constant.resolve().class_klass
        elif type(constant) == str:
            target = get_jstring(constant, frame.method.klass.loader)
        else:
            target = constant
        return target

    def push(self, frame, constant):
        frame.push(constant)

class Ldc(BaseLdc):
    def read_operand(self, reader):
        self.index = reader.read_uint(1)

class LdcW(BaseLdc):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

class Ldc2W(BaseLdc):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def push(self, frame, constant):
        frame.push2(constant)

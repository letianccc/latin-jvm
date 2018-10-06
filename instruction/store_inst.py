
from .instruction import Instruction, Poper2


class IStore(Instruction):
    def __init__(self, index):
        self.index = index

    def execute(self, frame):
        frame.store(self.index)

class IStore2(Instruction):
    def __init__(self, index):
        self.index = index

    def execute(self, frame):
        frame.store2(self.index)

class Store(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(1)

    def execute(self, frame):
        frame.store(self.index)

class Store2(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(1)

    def execute(self, frame):
        frame.store2(self.index)

class BaseArrayStore(Instruction):
    def execute(self, frame):
        e = self.get_element(frame)
        index = frame.pop()
        array = frame.pop()
        array.set_field(index, e)

class ArrayStore(BaseArrayStore):
    def get_element(self, frame):
        return frame.pop()

class ArrayStore2(BaseArrayStore):
    def get_element(self, frame):
        return frame.pop2()

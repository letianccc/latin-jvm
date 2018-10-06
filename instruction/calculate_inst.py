
from .instruction import Instruction, Poper2, Pusher2


class BaseAdd(Instruction):
    def execute(self, frame):
        operand2 = self.get_operand(frame)
        operand1 = self.get_operand(frame)
        result = operand1 + operand2
        self.push(frame, result)

class IAdd(BaseAdd):
    def get_operand(self, frame):
        return frame.pop()

    def push(self, frame, element):
        frame.push(element)

class IAdd2(BaseAdd):
    def get_operand(self, frame):
        return frame.pop2()

    def push(self, frame, element):
        frame.push2(element)

class BaseSub(Instruction):
    def execute(self, frame):
        operand2 = self.get_operand(frame)
        operand1 = self.get_operand(frame)
        result = operand1 - operand2
        self.push(frame, result)

class ISub(BaseSub):
    def get_operand(self, frame):
        return frame.pop()

    def push(self, frame, element):
        frame.push(element)

class ISub2(BaseSub):
    def get_operand(self, frame):
        return frame.pop2()

    def push(self, frame, element):
        frame.push2(element)

class IInc(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(1)
        self.constant = reader.read_uint(1)

    def execute(self, frame):
        var = frame.get_variable(self.index)
        result = var + self.constant
        frame.set_variable(self.index, result)

class BaseMul(Instruction):
    def execute(self, frame):
        operand2 = self.get_operand(frame)
        operand1 = self.get_operand(frame)
        result = operand1 * operand2
        self.push(frame, result)

class Mul(BaseMul):
    def get_operand(self, frame):
        return frame.pop()

    def push(self, frame, element):
        frame.push(element)

class Mul2(BaseMul):
    def get_operand(self, frame):
        return frame.pop2()

    def push(self, frame, element):
        frame.push2(element)


from .instruction import Instruction

class Branch(Instruction):
    def read_operand(self, reader):
        self.offset = reader.read_int(2)

    def jump(self, frame):
        pc = frame.get_start_pc()
        pc += self.offset
        frame.set_next_pc(pc)

class Goto(Branch):
    def execute(self, frame):
        self.jump(frame)

class IfCamp(Branch):
    def read_operands(self, frame):
        op2 = frame.pop()
        op1 = frame.pop()
        return op2, op1

class IfCampGt(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 > op2:
            self.jump(frame)

class IfCampEq(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 == op2:
            self.jump(frame)

class IfCampNe(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 != op2:
            self.jump(frame)

class IfCampLt(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 < op2:
            self.jump(frame)

class IfCampLe(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 <= op2:
            self.jump(frame)

class IfCampGt(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 > op2:
            self.jump(frame)

class IfCampGe(IfCamp):
    def execute(self, frame):
        op2, op1 = self.read_operands(frame)
        if op1 >= op2:
            self.jump(frame)

class IfEqual(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand == 0:
            self.jump(frame)

class IfNotEqual(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand != 0:
            self.jump(frame)

class IfGt(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand > 0:
            self.jump(frame)

class IfGe(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand >= 0:
            self.jump(frame)

class IfLt(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand < 0:
            self.jump(frame)

class IfLe(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand <= 0:
            self.jump(frame)

class IfNull(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand == None:
            self.jump(frame)

class IfNotNull(Branch):
    def execute(self, frame):
        operand = frame.pop()
        if operand != None:
            self.jump(frame)

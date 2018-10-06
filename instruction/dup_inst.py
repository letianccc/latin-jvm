
from .instruction import Instruction


class Dup(Instruction):
    def execute(self, frame):
        v = frame.pop()
        frame.push(v)
        frame.push(v)

class DupX1(Instruction):
    def execute(self, frame):
        v1 = frame.pop()
        v2 = frame.pop()
        frame.push(v1)
        frame.push(v2)
        frame.push(v1)

class DupX2(Instruction):
    def execute(self, frame):
        v1 = frame.pop()
        v2 = frame.pop()
        v3 = frame.pop()
        frame.push(v1)
        frame.push(v3)
        frame.push(v2)
        frame.push(v1)

class Dup2(Instruction):
    def execute(self, frame):
        v1 = frame.pop()
        v2 = frame.pop()
        frame.push(v2)
        frame.push(v1)
        frame.push(v2)
        frame.push(v1)

class Dup2X1(Instruction):
    def execute(self, frame):
        v1 = frame.pop()
        v2 = frame.pop()
        v3 = frame.pop()
        frame.push(v2)
        frame.push(v1)
        frame.push(v3)
        frame.push(v2)
        frame.push(v1)

class Dup2X2(Instruction):
    def execute(self, frame):
        v1 = frame.pop()
        v2 = frame.pop()
        v3 = frame.pop()
        v4 = frame.pop()
        frame.push(v2)
        frame.push(v1)
        frame.push(v4)
        frame.push(v3)
        frame.push(v2)
        frame.push(v1)



from .instruction import Instruction

class Cmp(Instruction):
    def execute(self, frame):
        operand2 = self.get_operand(frame)
        operand1 = self.get_operand(frame)
        result = self.compare(operand1, operand2)
        frame.push(result)

    def base_compare(self, operand1, operand2):
        if operand1 > operand2:
            result = 1
        elif operand1 == operand2:
            result = 0
        else:
            result = -1
        return result


class FCmp(Cmp):
    def __init__(self, is_g):
        self.is_g = is_g

    def get_operand(self, frame):
        return frame.pop()

    def compare(self, operand1, operand2):
        if not operand1 or not operand2:
            return 1 if self.is_g else -1
        return self.base_compare(operand1, operand2)



class LCmp(Cmp):
    def get_operand(self, frame):
        return frame.pop2()

    def compare(self, operand1, operand2):
        return self.base_compare(operand1, operand2)


class DCmp(Cmp):
    def __init__(self, is_g):
        self.is_g = is_g

    def get_operand(self, frame):
        return frame.pop2()

    def compare(self, operand1, operand2):
        if not operand1 or not operand2:
            return 1 if self.is_g else -1
        return self.base_compare(operand1, operand2)

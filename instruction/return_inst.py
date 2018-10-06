
from .instruction import Instruction

class BaseReturn(Instruction):
    def execute(self, frame):
        thread = frame.thread
        value = self.get_return_value(frame)
        self.return_value(thread, value)

    def return_value(self, thread, value):
        thread.pop_frame()
        invoker = thread.current_frame()
        self.load(invoker, value)

class ReturnVoid(BaseReturn):
    def get_return_value(self, frame):
        return None

    def load(self, frame, value):
        pass

class Return(BaseReturn):
    def get_return_value(self, frame):
        v = frame.pop()
        return v

    def load(self, frame, value):
        frame.push(value)

class Return2(BaseReturn):
    def get_return_value(self, frame):
        v = frame.pop2()
        return v

    def load(self, frame, value):
        frame.push2(value)



class Poper1:
    def pop(self, frame):
        return frame.pop()

class Poper2:
    def pop(self, frame):
        return frame.pop2()

class Pusher1:
    def push(self, frame, element):
        return frame.push(element)

class Pusher2:
    def push(self, frame, element):
        return frame.push2(element)

class Instruction:
    def __init__(self):
        self.poper = Poper1()
        self.pusher = Pusher1()

    def execute(self, frame):
        pass

    def read_operand(self, reader):
        pass

    def pop(self, frame):
        return frame.pop()

    def push(self, frame, element):
        return frame.push(element)

class NOP(Instruction):
    pass



class Bipush(Instruction):
    def read_operand(self, reader):
        self.operand = reader.read_uint(1)

    def execute(self, frame):
        frame.push(self.operand)

class Sipush(Instruction):
    def read_operand(self, reader):
        self.operand = reader.read_uint(2)

    def execute(self, frame):
        frame.push(self.operand)

class Pop(Instruction):
    def execute(self, frame):
        frame.pop()

class Pop2(Instruction):
    def execute(self, frame):
        frame.pop()
        frame.pop()


class Swap(Instruction):
    def execute(self, frame):
        v1 = frame.pop()
        v2 = frame.pop()
        frame.push(v1)
        frame.push(v2)

class ArrayLength(Instruction):
    def execute(self, frame):
        arr_ref = frame.pop()
        n = arr_ref.get_array_length()
        frame.push(n)

class Instantceof(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def execute(self, frame):
        obj = frame.pop()
        if not obj:
            frame.push(0)

        classref = frame.get_constant(self.index)
        cs = classref.resolve()
        if obj.is_instance_of(cs):
            frame.push(1)
        else:
            frame.push(0)


class CheckCast(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def execute(self, frame):
        obj = frame.pop()
        frame.push(obj)
        if not obj:
            return

        classref = frame.get_constant(self.index)
        cs = classref.resolve()
        if not obj.is_instance_of(cs):
            raise Exception('caseException')

class Initializer:
    def init(self, thread, klass):
        self.init_class(thread, klass)
        return

    def init_class(self, thread, klass):
        klass.init()
        frame = thread.current_frame()
        self.schedule_clinit(thread, klass)
        self.init_superclass(thread, klass)
        thread.execute(frame)

    def schedule_clinit(self, thread, klass):
        clinit_method = klass.get_clinit_method()
        if clinit_method:
            thread.create_frame(clinit_method)

    def init_superclass(self, thread, klass):
        # is_interface
        superclass = klass.superclass
        if superclass and not superclass.init_start:
            self.init_class(thread, superclass)

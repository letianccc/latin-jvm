
from old_jvm1.utils.reader import CodeReader
from old_jvm1.instruction import *
from old_jvm1.utils.factory import inst_factory

class Thread:
    def __init__(self, max_size=50):
        self.frames = []
        self.max_size = max_size
        self.prints = []

    def push_frame(self, frame):
        if len(self.frames) == self.max_size:
            raise Exception('stack full', 'max_size: ', self.max_size, '\tcur_size', len(self.frames))
        self.frames.append(frame)

    def pop_frame(self):
        return self.frames.pop()

    def current_frame(self):
        if len(self.frames) == 0:
            return None
        return self.frames[-1]

    def new_frame(self, method):
        f = Frame(method, self)
        return f

    def create_frame(self, method, args=[]):
        f = self.new_frame(method)
        for i in range(len(args)):
            arg = args[i]
            f.set_variable(i, arg)
        self.push_frame(f)
        return f

    def execute(self, start_frame=None):
        frame = self.current_frame()
        while frame != start_frame:
            frame.execute()
            if self.is_stack_empty():
                log('\nfinish!!!!!!')
                log(frame.local_vars)
                return frame
            frame = self.current_frame()

    def is_stack_empty(self):
        return len(self.frames) == 0

class Frame:
    def __init__(self, method, thread):
        self.max_local = method.max_locals
        self.max_stack = method.max_stack
        self.local_vars = [None] * self.max_local
        self.operand_stack = []
        self.next_pc = 0
        self.start_pc = 0
        self.method = method
        self.thread = thread
        self.reader = CodeReader(method.bytecode)

    def execute(self):
        inst = self.get_instruction()
        self.set_next_pc(self.reader.get_next_pc())
        inst.execute(self)
        self.pc_proceed()

    def get_instruction(self):
        opcode = self.get_next_opcode()
        inst = inst_factory.get(opcode, None)
        if not inst:
            log('\nexception\npc: ' + str(self.get_start_pc()) + '\topcode: ' + hex(opcode))
            raise Exception
        inst.read_operand(self.reader)

        log('class: ', self.method.get_class_name(), '\tmethod:',self.method.name + ' ' + self.method.desc, 'inst: ', inst.__class__.__name__, '\tpc: ', str(self.get_start_pc()), '\topcode', hex(opcode))
        # log('stack: ', self.operand_stack)
        # log('local: ', self.local_vars)

        return inst

    def get_next_opcode(self):
        pc = self.get_next_pc()
        self.reader.set_next_pc(pc)
        opcode = self.reader.get_opcode()
        return opcode

    def get_variable(self, index):
        return self.local_vars[index]

    def set_variable(self, index, variable):
        self.local_vars[index] = variable

    def get_this(self):
        return self.get_variable(0)

    def get_from_stack(self, index):
        return self.operand_stack[index]

    def store(self, index):
        operand = self.pop()
        self.set_variable(index, operand)

    def store2(self, index):
        operand = self.pop2()
        self.set_variable(index, operand)

    def load(self, index):
        operand = self.get_variable(index)
        self.push(operand)

    def load2(self, index):
        operand = self.get_variable(index)
        self.push2(operand)

    def push(self, operand):
        self.operand_stack.append(operand)

    def push2(self, operand):
        self.operand_stack.append(operand)
        self.operand_stack.append(None)

    def pop(self):
        return self.operand_stack.pop()

    def pop2(self):
        self.operand_stack.pop()
        v = self.operand_stack.pop()
        return v

    def pc_proceed(self):
        self.start_pc = self.next_pc

    def get_next_pc(self):
        return self.next_pc

    def set_next_pc(self, pc):
        self.next_pc = pc

    def get_start_pc(self):
        return self.start_pc

    def get_constant(self, index):
        cp = self.method.get_constants()
        return cp.get_constant(index)

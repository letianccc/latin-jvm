
from .instruction import Instruction, Initializer



class FieldInstruction(Instruction):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def get_field(self, frame):
        cp = frame.method.get_constants()
        field_ref = cp.get_constant(self.index)
        field = field_ref.resolve_field()
        return field

    def execute(self, frame):
        field = self.get_field(frame)
        self.check(frame, field)
        self.execute_operation(frame, field)

class StaticFieldInstruction(FieldInstruction):
    def check(self, frame, field):
        self.check_access_flag(field)
        self.check_initial(frame, field.klass)

    def check_access_flag(self, field):
        if not field.is_static():
            raise Exception('not static')

    def check_initial(self, frame, klass):
        if not klass.init_start:
            initializer = Initializer()
            initializer.init(frame.thread, klass)

class InstanceFieldInstruction(FieldInstruction):
    def check(self, frame, field):
        self.check_access_flag(field)

    def check_access_flag(self, field):
        if field.is_static():
            raise Exception('is static')

class GetStatic(StaticFieldInstruction):
    def execute_operation(self, frame, field):
        v = self.get_field_value(field)
        self.load(frame, field, v)

    def get_field_value(self, field):
        klass = field.klass
        v = klass.get_static_field(field.id)
        return v

    def load(self, frame, field, value):
        if field.is_big_field():
            frame.push2(value)
        else:
            frame.push(value)

class GetField(InstanceFieldInstruction):
    def execute_operation(self, frame, field):
        v = self.get_field_value(frame, field)
        self.load(frame, field, v)

    def get_field_value(self, frame, field):
        obj = frame.pop()
        v = obj.get_field(field.id)
        return v

    def load(self, frame, field, value):
        if field.is_big_field():
            frame.push2(value)
        else:
            frame.push(value)

class PutStatic(StaticFieldInstruction):
    def execute_operation(self, frame, field):
        v = self.get_field_value(frame, field)
        self.store(field, v)

    def get_field_value(self, frame, field):
        if field.is_big_field():
            v = frame.pop2()
        else:
            v = frame.pop()
        return v

    def store(self, field, value):
        klass = field.klass
        klass.set_static_field(field.id, value)

class PutField(InstanceFieldInstruction):
    def execute_operation(self, frame, field):
        v = self.get_field_value(frame, field)
        self.store(frame, field, v)

    def get_field_value(self, frame, field):
        if field.is_big_field():
            v = frame.pop2()
        else:
            v = frame.pop()
        return v

    def store(self, frame, field, value):
        obj = frame.pop()
        obj.set_field(field.id, value)

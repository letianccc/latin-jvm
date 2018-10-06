
from .instruction import Instruction, Initializer
from old_jvm1.debug.util import log
from .native_method import find_method

class InvokeLogic(Instruction):
    def invoke_method(self, invoke_frame, method):
        t = invoke_frame.thread
        args = self.get_args(invoke_frame, method)
        t.create_frame(method, args)

    def get_args(self, invoke_frame, method):
        args = []
        count = method.get_arguments_length()
        for i in range(count):
            v = invoke_frame.pop()
            args.insert(0, v)
        return args

    def get_method(self, frame):
        cp = frame.method.get_constants()
        method_ref = cp.get_constant(self.index)
        method = method_ref.resolve()
        return method

class InvokeStatic(InvokeLogic):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def execute(self, frame):
        method = self.get_method(frame)
        klass = method.klass
        self.check_class_init(klass, frame)
        self.invoke_method(frame, method)

    def check_class_init(self, klass, frame):
        if not klass.init_start:
            initializer = Initializer()
            initializer.init(frame.thread, klass)

class InvokeSpecial(InvokeLogic):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def execute(self, frame):
        method = self.get_method(frame)

        if method.is_static():
            raise Exception('should not static')

        self.invoke_method(frame, method)

class InvokeVirtual(InvokeLogic):
    def read_operand(self, reader):
        self.index = reader.read_uint(2)

    def execute(self, frame):
        method = self.get_method(frame)
        count = method.get_arguments_length()
        objref = frame.get_from_stack(-count)

        # error:  objref.klass.name 是 Object 应该是 Class

        if objref.__class__.__name__ != 'Object':
            if method.name == 'println':
                self.println(frame, method)
                return
            raise Exception('objref is None! methodname: ', method.name)

        target_method = objref.klass.find_method(method.name, method.desc)
        self.invoke_method(frame, target_method)

    def println(self, frame, method):
        desc = method.desc
        if desc in ['(Z)V', '(C)V', '(I)V', '(B)V', '(S)V', '(F)V']:
            output = frame.pop()
        elif desc in ['(J)V', '(D)V']:
            output = frame.pop2()
        elif desc == '(Ljava/lang/String;)V':
            jstring = frame.pop()
            output = jstring.get_value()
        else:
            raise Exception('method_name: ' + method.name + '\tdesc:' + desc)
        log('println:  ', output)
        frame.thread.prints.append(output)
        frame.pop()


class InvokeNative(InvokeLogic):
    def execute(self, frame):
        method = frame.method
        class_name = method.klass.name
        native_method = find_method(class_name, method.name, method.desc)
        if not native_method:
            raise Exception('native_method classname: ' + class_name + '\tmethodname: '+ method.name)
        native_method(frame)

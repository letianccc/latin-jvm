

from old_jvm1.core.class_loader import *
from old_jvm1.core.runtime_data import *


class JVM:
    def __init__(self):
        self.loader = Loader()

    def run(self, qualified_name, args=None):
        klass = self.loader.load(qualified_name)
        m = klass.get_main_method()
        if m:
            return self.execute(m, args)
        else:
            raise Exception("main method not found")

    def execute(self, method, args):
        t = Thread()
        f = t.create_frame(method)
        if args:
            arr = create_args_array(args)
            f.set_variable(0, arr)
        main_frame = t.execute()
        return main_frame

    def create_args_array(self, args):
        str_class = self.loader.load('java/lang/String')
        arr_obj = str_class.get_array_class().new_array(len(args))
        for i in range(len(args)):
            arg = args[i]
            ref = get_jstring(arg)
            arr_obj.fields[i] = ref
        return arr_obj

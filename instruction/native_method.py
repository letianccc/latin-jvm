from old_jvm1.utils.jstring import *


methods = {}


def get_class(frame):
    this = frame.get_this()
    class_klass = this.klass.class_klass
    frame.push(class_klass)

def get_primitive_class_klass(frame):
    jstring = frame.get_variable(0)
    class_name = jstring.get_value()
    referenced_klass = frame.method.klass
    klass = referenced_klass.load(class_name)
    class_klass = klass.class_klass
    frame.push(class_klass)

#error
def get_name(frame):
    class_object = frame.get_this()
    klass = class_object.extra
    name = klass.name.replace('/', '.')
    loader = frame.method.klass.loader
    jstring = get_jstring(name, loader)
    frame.push(jstring)

def desired_assertion_status0(frame):
    frame.push(False)

def empty_native_method(frame):
    pass

def register_methods():
    register('java/lang/Object', 'getClass', '()Ljava/lang/Class;', get_class)
    register('java/lang/Class', 'getName0', '()Ljava/lang/String;', get_name)
    register('java/lang/Class', 'getPrimitiveClass', '(Ljava/lang/String;)Ljava/lang/Class;', get_primitive_class_klass)
    register('java/lang/Class', 'desiredAssertionStatus0', '(Ljava/lang/Class;)Z', desired_assertion_status0)

def register(class_name, method_name, method_desc, native_method):
    connector = '~'
    k = connector.join([class_name, method_name, method_desc])
    methods[k] = native_method

def find_method(class_name, method_name, method_desc):
    connector = '~'
    k = connector.join([class_name, method_name, method_desc])
    if k in methods:
        return methods[k]
    if method_desc == '()V' and method_name == 'registerNatives':
        return empty_native_method
    return None

register_methods()


from old_jvm1.core.classfile import *
from old_jvm1.core.klass import *
from old_jvm1.utils.reader import *
from old_jvm1.core.jvm import JVM

def execute(qualified_name):
    jvm = JVM()
    main_frame = jvm.run(qualified_name)
    return main_frame

def get_classfile(class_name):
    reader = FileReader()
    data = reader.read(class_name)
    cf = ClassFile(data)
    return cf

def get_struct(class_name):
    cf = get_classfile(class_name)
    struct = Klass(cf)
    return struct

def log_object_fields(o):
    for f in o.fields:
        print(f)

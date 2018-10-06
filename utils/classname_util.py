
from old_jvm1.utils.enum1 import ArrayType


array_type_to_classname = {
    ArrayType.BOOLEAN.value: '[Z',
    ArrayType.CHAR.value: '[C',
    ArrayType.FLOAT.value: '[F',
    ArrayType.DOUBLE.value: '[D',
    ArrayType.BYTE.value: '[B',
    ArrayType.SHORT.value: '[S',
    ArrayType.INT.value: '[I',
    ArrayType.LONG.value: '[J',
}

primitive = {
        'V': 'void',
        'Z': 'boolean',
        'B': 'byte',
        'S': 'short',
        'I': 'int',
        'J': 'long',
        'C': 'char',
        'F': 'float',
        'D': 'double'
}



def get_classname(desc):
    if desc[0] == '[':
        return desc
    if desc[0] == 'L':
        return desc[1:-1]
    classname = primitive[desc]
    return classname

def get_desc(classname):
    if classname[0] == '[':
        return classname
    for desc, name in primitive.items():
        if name == classname:
            return desc
    return 'L' + classname + ';'

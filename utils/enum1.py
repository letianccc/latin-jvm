
from enum import Enum

class ConstantType(Enum):
     Class = 7
     Fieldref = 9
     Methodref = 10
     InterfaceMethodref = 11
     String = 8
     Integer = 3
     Float = 4
     Long = 5
     Double = 6
     NameAndType = 12
     Utf8 = 1
     MethodHandle = 15
     MethodType = 16
     InvokeDynamic = 18

class AccessType(Enum):
    PUBLIC       = 0x0001
    PRIVATE      = 0x0002
    PROTECTED    = 0x0004
    STATIC       = 0x0008
    FINAL        = 0x0010
    SUPER        = 0x0020
    SYNCHRONIZED = 0x0020
    VOLATILE     = 0x0040
    BRIDGE       = 0x0040
    TRANSIENT    = 0x0080
    VARARGS      = 0x0080
    NATIVE       = 0x0100
    INTERFACE    = 0x0200
    ABSTRACT     = 0x0400
    STRICT       = 0x0800
    SYNTHETIC    = 0x1000
    ANNOTATION   = 0x2000
    ENUM         = 0x4000

class ArrayType(Enum):
     BOOLEAN = 4
     CHAR = 5
     FLOAT = 6
     DOUBLE = 7
     BYTE = 8
     SHORT = 9
     INT = 10
     LONG = 11

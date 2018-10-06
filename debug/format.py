
import os
from old_jvm1.debug.util import log
from old_jvm1.core.jvm import JVM

def print_classfile(classfile):
    log('version:\t' + str(classfile.major_version) + '.' + str(classfile.minor_version))
    log('constant_count:\t' + str(len(classfile.constant_pool)))
    log('access_flag:\t' + hex(classfile.class_access))
    log('this_class:\t' + classfile.constant_pool[classfile.this_class-1].get_value())
    if classfile.super_class != 0:
        log('super_class:\t' + classfile.constant_pool[classfile.super_class-1].get_value())
    log('interfaces:\n')
    for i in classfile.interfaces:
        log(classfile.constant_pool[i])
        log()
    log()

    log('fields:\n')
    log('length:\t' + str(len(classfile.fields)))
    for f in classfile.fields:
        log('name:\t' + f.get_name())
        for attr in f.attributes:
            log(attr.__class__.__name__)
        log()
    log()

    log('methods:\n')
    log('length:\t' + str(len(classfile.methods)))
    for m in classfile.methods:
        log('name:\t' + m.get_name())
        for attr in m.attributes:
            log(attr.__class__.__name__)
        log()
    log()

    log('attributes:\n')
    for attr in classfile.attributes:
        log(attr.__class__.__name__)

def format_class_file(classfile_path, output_path):
    classfile_path += '.class'
    with open(classfile_path, 'rb') as fin:
        with open(output_path, 'w') as fout:
            col = 0
            while True:
                if col % 16 == 0:
                    start_line = '{:0<#4x}'.format(col) + '\t\t'
                    fout.write(start_line)

                byte = fin.read(1)
                if byte == b'':
                    break
                hex_byte = byte.hex()
                text = hex_byte + '\t'
                fout.write(text)
                col += 1

                if col % 16 == 0:
                    fout.write('\n')

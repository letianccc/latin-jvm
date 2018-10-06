

import os
import subprocess


def javac(dir, filename):
    command = ['javac ' + filename]
    a = subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=dir)

def javac_all():
    dirname = '/home/latin/code/latin/python/latin_jvm/javacase'
    javafiles = os.listdir(dirname)
    for filename in javafiles:
        if filename.endswith('.java'):
            javac(dirname, filename)
    # command = ['javac ' + 'InvokeVirtualTest.java']
    # a = subprocess.run(command, shell=True, stdout=subprocess.PIPE, cwd=dirname)

def javac1():
    dirname = '/home/latin/code/latin/python/latin_jvm/javacase'
    filename = dirname + '/Test.java'
    javac(dirname, filename)

# javac_all()
javac1()

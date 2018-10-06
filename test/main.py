from old_jvm1.utils import config

config.test_state = True
import unittest
from testutil import *
# from old_jvm1.util import main

class TestJVM(unittest.TestCase):
    def test_klass(self):
        class_name = 'java/lang/Object'
        struct = get_struct(class_name)
        cp = struct.constant_pool
        self.assertEqual(cp.get_constant(18), '<init>')
        self.assertEqual(cp.get_constant(6), '@')
        self.assertEqual(cp.get_constant(57).get_type(), 'ClassRef')

        method = struct.methods[2]
        self.assertEqual(method.desc, '()Ljava/lang/Class;')
        self.assertEqual(method.name, 'getClass')
        self.assertEqual(method.max_stack, 4)

    def test_array(self):
        class_name = 'BubbleSortTest'
        main_frame = execute(class_name)
        variables = main_frame.local_vars
        expect_list = [9, 10, 11, 22, 24, 36, 36, 48, 56,
            65, 77, 78, 84, 92, 95, 97]
        array = main_frame.local_vars[1]
        for i in range(len(expect_list)):
            expect_e = expect_list[i]
            e = array.get_field(i)
            self.assertEqual(expect_e, e)
            self.assertEqual(type(e), int)

        class_name = 'BubbleSortTest2'
        main_frame = execute(class_name)
        array = main_frame.local_vars[1]
        expect_list = [9.0, 10.0, 11.0, 22.0, 24.0, 36.0, 36.0, 48.0, 56.0,
            65.0, 77.0, 78.0, 84.0, 92.0, 95.0, 97.0]
        for i in range(len(expect_list)):
            expect_e = expect_list[i]
            e = array.get_field(i)
            self.assertEqual(expect_e, e)
            self.assertEqual(type(e), float)

    def test_multiarray(self):
        class_name = 'Array3D'
        main_frame = execute(class_name)
        array = main_frame.local_vars[1]
        for i in range(5):
            for j in range(4):
                for k in range(3):
                    v = array.get_field(i).get_field(j).get_field(k)
                    target = i + j + k
                    self.assertEqual(v, target)

    def test_cmp(self):
        class_name = 'CmpTest'
        main_frame = execute(class_name)
        variables = main_frame.local_vars
        expect_list = [None, 1, 2, 3.0, 0, 0, 1, 1, None,
            2.0, None, 3.0, None, 0, 0, 1, 1, None,
            2, None, 3, None, 0, 0, 1]

        for i in range(len(expect_list)):
            expect_e = expect_list[i]
            e = variables[i]
            self.assertEqual(expect_e, e)

    def test_field(self):
        class_name = 'MyObject'
        main_frame = execute(class_name)
        variables = main_frame.local_vars
        o = variables[2]
        self.assertEqual(o.klass.static_field_values[0], 32768)
        self.assertEqual(o.get_field(0), 32768)

    def test_invoke_virtual(self):
        class_name = 'InvokeVirtualTest'
        main_frame = execute(class_name)
        variables = main_frame.local_vars
        o1 = variables[1]
        o2 = variables[2]
        self.assertEqual(o1.get_field(0), 4.2)
        self.assertEqual(o1.get_field(2), 4.4)
        self.assertEqual(o2.get_field(0), 9.3)
        self.assertEqual(o2.get_field(2), 9.600000000000001)
        self.assertEqual(o2.get_field(4), 9.899999999999999)

    def test_invoke_special(self):
        class_name = 'InvokeSpecialTest'
        main_frame = execute(class_name)
        variables = main_frame.local_vars
        o1 = variables[1]
        o2 = variables[2]
        self.assertEqual(o1.get_field(0), 2.1)
        self.assertEqual(o1.get_field(2), 2.2)
        self.assertEqual(o2.get_field(0), 3.1)
        self.assertEqual(o2.get_field(2), 3.2)
        self.assertEqual(o2.get_field(4), 3.3)

    def test_string(self):
        class_name = 'StringTest'
        main_frame = execute(class_name)
        variables = main_frame.local_vars
        jstring = variables[1]
        self.assertEqual(jstring.get_value(), 'xyz')
        test_klass = jstring.klass.loader.class_list['StringTest']
        static_jstring = test_klass.static_field_values[0]
        self.assertEqual(static_jstring.get_value(), 'abc')

    def test_class_klass(self):
        class_name = 'GetClassTest'
        main_frame = execute(class_name)
        prints = main_frame.thread.prints
        target = ['void', 'boolean', 'byte', 'char', 'short',
            'int', 'long', 'float', 'double', 'java.lang.Object',
            'GetClassTest', '[I', '[[I', '[Ljava.lang.Object;',
            '[[Ljava.lang.Object;', 'java.lang.Runnable', 'java.lang.String',
             '[D', '[Ljava.lang.String;']
        for i in range(len(target)):
            t = target[i]
            output = prints[i]
            self.assertEqual(output, t)

if __name__ == '__main__':
    unittest.execute()

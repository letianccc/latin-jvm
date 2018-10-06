from old_jvm1.utils import config
config.test_state = True
import unittest
from testutil import *
# from old_jvm1.util import main

class TestJVM(unittest.TestCase):
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



if __name__ == '__main__':
    unittest.main()

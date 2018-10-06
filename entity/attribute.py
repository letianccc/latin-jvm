
class Attribute:
    def is_type(self, attribute_type):
        name = self.__class__.__name__
        return name == attribute_type

class SourceFileAttribute(Attribute):
    def read_info(self, reader):
        reader.read_int(4)
        self.index = reader.read_int(2)


class ConstantValueAttribute(Attribute):
    def __init__(self):
        self.index = None

    def read_info(self, reader):
        attr_len = reader.read_int(4)
        self.index = reader.read_int(2)

class DeprecatedAttribute(Attribute):
    def read_info(self, reader):
        reader.read_int(4)


class SyntheticAttribute(Attribute):
    def read_info(self, reader):
        reader.read_int(4)



class CodeAttribute(Attribute):
    def read_info(self, reader, constant_pool):
        reader.read_int(4)
        self.max_stack = reader.read_int(2)
        self.max_locals = reader.read_int(2)
        code_len = reader.read_int(4)
        self.bytecode = reader.read_bytes(code_len)
        self.exception_table = self.get_exception_table(reader)
        self.attributes = reader.read_attributes(constant_pool)

    def get_exception_table(self, reader):
        table = []
        table_len = reader.read_int(2)
        for i in range(table_len):
            e = ExceptionEntry()
            e.read_info(reader)
            table.append(e)
        return table

    def get_max_locals(self):
        return self.max_locals

    def get_max_stack(self):
        return self.max_stack

    def get_bytecode(self):
        return self.bytecode


class ExceptionEntry(Attribute):
    def read_info(self, reader):
        self.start_pc = reader.read_int(2)
        self.end_pc = reader.read_int(2)
        self.handle_pc = reader.read_int(2)
        self.catch_type = reader.read_int(2)

class ExceptionsAttribute(Attribute):
    def read_info(self, reader):
        reader.read_int(4)
        self.index_table = reader.read_ints(2)

class LineNumberTableAttribute(Attribute):
    def read_info(self, reader):
        reader.read_int(4)
        table = []
        table_len = reader.read_int(2)
        for i in range(table_len):
            e = LineNumberEntry()
            e.read_info(reader)
            table.append(e)
        self.table = table

class LineNumberEntry(Attribute):
    def read_info(self, reader):
        self.start_pc = reader.read_int(2)
        self.line_number = reader.read_int(2)

class UnparseAttribute(Attribute):
    def read_info(self, reader):
        length = reader.read_int(4)
        self.info = reader.read_bytes(length)

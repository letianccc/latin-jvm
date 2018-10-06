from old_jvm1.entity.object import Object

string_pool = dict()
def get_jstring(pystring, loader):
    if pystring in string_pool:
        return string_pool[pystring]
    jstring = convert(pystring, loader)
    string_pool[pystring] = jstring
    return jstring

def convert(pystring, loader):
    pystring = pystring.encode('utf16')
    char_klass = loader.load('[C')
    chars = Object(char_klass)
    chars.fields = pystring

    str_klass = loader.load('java/lang/String')
    jstring = str_klass.new_object()
    jstring.set_ref_var('value', '[C', chars)
    return jstring




def walk():
    dirname = '/home/latin/code/latin/python/latin_jvm/javacase'
    names = []
    for name in os.listdir(dirname):
        if name.endswith('.java'):
            qualified_name = name[:-5]
            names.append(qualified_name)
    jvm = JVM()
    for name in names:
        log('\t' + name)
        jvm.run(name)

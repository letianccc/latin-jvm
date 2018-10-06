
from old_jvm1.core.jvm import JVM

if __name__ == '__main__':
    jvm = JVM()
    qualified_name = 'Test'
    jvm.run(qualified_name)

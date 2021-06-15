import os
import sys
from CompilationEngine import CompilationEngine

if __name__ == '__main__':
    directory = sys.argv[1]
    if os.path.isdir(directory):
        entries = os.listdir(directory)
        for entry in entries:
            if ".jack" in entry:
                xml_file_name = os.path.abspath(os.path.join(directory, entry)) \
                                    .replace(".jack", "") + ".vm"
                CompilationEngine(os.path.abspath(os.path.join(directory, entry)), xml_file_name)
    else:
        xml_file_name = directory.replace(".jack", "") + ".vm"
        CompilationEngine(directory, xml_file_name)

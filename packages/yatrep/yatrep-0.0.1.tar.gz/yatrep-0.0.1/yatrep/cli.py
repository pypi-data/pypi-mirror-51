import xml.etree.ElementTree as ET
import sys

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    OKBLUE = '\033[94m'
    BOLD = '\033[1m'
    HEADER = '\033[95m'
    NORMAL = '\033[0m'


class Yatrep():
    def parse_xml(file_path):
        print("Parsing file '{0}'".format(file_path))
        root = ET.parse(file_path).getroot()
        return TestResults(root)


class TestResults():
    def __init__(self, xml_root):
        self.failed_tests = int(xml_root.attrib['failed'])
        self.passed_tests = int(xml_root.attrib['passed'])
        self.total_tests = int(xml_root.attrib['total'])
        self.test_duration = float(xml_root.attrib['duration'])
        self.check_success()

    def check_success(self):
        if (self.failed_tests == 0 and self.total_tests == self.passed_tests):
            self.success = True
        else:
            self.success = False


if __name__ == '__main__':
    main()

def main():
    if (len(sys.argv) < 1):
        print("Invalid usage.")
        print("Example: .'/bin/yatrep.sh path_to_file'")
        sys.exit(-1)
    else:
        result = Yatrep.parse_xml(sys.argv[1])
        exit_code = 0
        if result.success == False:
            exit_code = -1
            print("{1}Tests failed!".format(bcolors.FAIL))
        else:
            print("{0}Tests passed!".format(bcolors.OKGREEN))
        print(bcolors.NORMAL)
        print("{0}Total: {1}".format(bcolors.BOLD, result.total_tests))
        print("{0}Passed: {1}".format(bcolors.BOLD, result.passed_tests))

        error_color = bcolors.NORMAL
        if (result.failed_tests > 0):
            error_color = bcolors.FAIL

        print("{2}{0}Failed: {1}".format(bcolors.BOLD, result.failed_tests, error_color))
        sys.exit(exit_code)

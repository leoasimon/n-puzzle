from io import StringIO
from os import getcwd, listdir
from os.path import join
import sys
from unittest import TestCase
from unittest.mock import patch
sys.path.insert(0, join(getcwd(), "../"))
from parser import parsefile

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Parser(TestCase):
    def test_invalid(self):
        print(bcolors.HEADER + "-----INVALID FILES-----")
        files = listdir(join(getcwd(), "puzzles/invalids"))
        for fname in files:
            print(bcolors.OKBLUE + fname)
            path = join(getcwd(), "puzzles/invalids", fname)
            with patch('sys.stderr', new=StringIO()) as fake_out:
                res = parsefile(path)
                if res == None:
                    print(bcolors.OKGREEN + "OK: " + fake_out.getvalue())
                else:
                    print(bcolors.FAIL + "KO")
    def test(self):
        self.test_invalid()

if __name__ == "__main__":
    parser = Parser()
    parser.test()
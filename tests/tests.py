#! /usr/bin/env python3

from io import StringIO
from os import getcwd, listdir
from os.path import join, dirname, realpath
import sys
import subprocess
from unittest import TestCase
from unittest.mock import patch
sys.path.insert(0, join(getcwd(), "../"))
from parser import parsefile

dir_path = dirname(realpath(__file__))
p_path = join(dir_path, "../n-puzzle.py")
print(p_path)

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

class Main(TestCase):
    def test_main(self):
        print(bcolors.HEADER + "-----VALIDS-----")
        files = listdir(join(getcwd(), "puzzles/valids"))
        for fname in files:
            print(bcolors.OKBLUE + fname)
            path = join(getcwd(), "puzzles/valids", fname)
            out1 = subprocess.check_output([p_path, path])
            print(out1.decode())
    def test(self):
        self.test_main()

        

if __name__ == "__main__":
    allargs = ["parser", "main"]
    args = [e for e in sys.argv if e in allargs]
    args = allargs if len(args) == 0 else args

    if "parser" in args:
        parser = Parser()
        parser.test()
    
    if "main" in args:
        main = Main()
        main.test()
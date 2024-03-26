import unittest
import sys
import os

if __name__ == "__main__":
    # use mpremote mount to test without copying testfiles to Pico
    # mpremote mount ./tests exec "import sys; sys.path.append('/');sys.path.append('..');" run test.py
    unittest.main("tests")

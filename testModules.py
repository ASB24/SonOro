import sys
sys.path.append('./modules')
sys.path.append('./modules/tests')

if True:  # noqa: E402
    import unittest
    from FileCheckerTesting import TestMethods as FileChecker


if __name__ == '__main__':
    unittest.main(verbosity=3)

import unittest

from source_policy import screen_source


class SourcePolicyTests(unittest.TestCase):
    def test_standard_library_algorithm_is_accepted(self):
        result = screen_source("import heapq\ndef solve(n, edges, s, t): return 0\n")
        self.assertTrue(result.accepted)
        self.assertEqual(result.reasons, ())

    def test_file_process_and_network_capabilities_are_rejected(self):
        for source in (
            "def solve(*a): return open('x').read()",
            "import pathlib\ndef solve(*a): return 0",
            "import subprocess\ndef solve(*a): return 0",
            "import socket\ndef solve(*a): return 0",
            "def solve(*a): return __import__('os')",
        ):
            with self.subTest(source=source):
                self.assertFalse(screen_source(source).accepted)

    def test_syntax_failure_is_a_recordable_rejection(self):
        result = screen_source("def solve(:")
        self.assertFalse(result.accepted)
        self.assertTrue(result.reasons[0].startswith("syntax:"))


if __name__ == "__main__":
    unittest.main()

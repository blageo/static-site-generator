import unittest
import os
import shutil
import tempfile
from main import copy_static, extract_title

class TestCopyStatic(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.src = os.path.join(self.temp_dir, "src")
        self.dst = os.path.join(self.temp_dir, "dst")
        os.makedirs(self.src)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_copy_static_single_file(self):
        with open(os.path.join(self.src, "test.txt"), "w") as f:
            f.write("test content")
        copy_static(self.src, self.dst)
        self.assertTrue(os.path.exists(os.path.join(self.dst, "test.txt")))
        with open(os.path.join(self.dst, "test.txt")) as f:
            self.assertEqual(f.read(), "test content")

    def test_copy_static_multiple_files(self):
        for i in range(3):
            with open(os.path.join(self.src, f"file{i}.txt"), "w") as f:
                f.write(f"content{i}")
        copy_static(self.src, self.dst)
        for i in range(3):
            self.assertTrue(os.path.exists(os.path.join(self.dst, f"file{i}.txt")))

    def test_copy_static_nested_directories(self):
        subdir = os.path.join(self.src, "subdir")
        os.makedirs(subdir)
        with open(os.path.join(subdir, "nested.txt"), "w") as f:
            f.write("nested")
        copy_static(self.src, self.dst)
        self.assertTrue(os.path.exists(os.path.join(self.dst, "subdir", "nested.txt")))

    def test_copy_static_removes_existing_destination(self):
        os.makedirs(self.dst)
        with open(os.path.join(self.dst, "old.txt"), "w") as f:
            f.write("old")
        with open(os.path.join(self.src, "new.txt"), "w") as f:
            f.write("new")
        copy_static(self.src, self.dst)
        self.assertFalse(os.path.exists(os.path.join(self.dst, "old.txt")))
        self.assertTrue(os.path.exists(os.path.join(self.dst, "new.txt")))


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_single_h1(self):
        markdown = "# Hello World"
        self.assertEqual(extract_title(markdown), "Hello World")

    def test_extract_title_with_extra_spaces(self):
        markdown = "#   Multiple   Spaces   "
        self.assertEqual(extract_title(markdown), "Multiple   Spaces")

    def test_extract_title_multiple_lines(self):
        markdown = "Some text\n# My Title\nMore text"
        self.assertEqual(extract_title(markdown), "My Title")

    def test_extract_title_not_found(self):
        markdown = "## Not a title\n### Also not"
        with self.assertRaises(Exception):
            extract_title(markdown)

    def test_extract_title_empty_string(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)


if __name__ == "__main__":
    unittest.main()
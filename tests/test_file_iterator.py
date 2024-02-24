import pytest
from file_iterator import FileIterator
from icecream import ic


def test_file_iterator():
    file_iter = FileIterator("tests/data/test_dir_tree")
    files = list(file_iter.walk())
    ic(files)
    assert len(files) == 10
    assert "tests/data/test_dir_tree/p2/p22/file22.ext2" in files


def test_file_iterator_filter():
    file_iter = FileIterator("tests/data/test_dir_tree")
    files = list(file_iter.filter_by_extension(["ext1"]).walk())
    ic(files)
    assert len(files) == 4
    assert "tests/data/test_dir_tree/p1/p11/file11.ext1" in files
    assert "tests/data/test_dir_tree/p2/p22/file22.ext1" in files


def test_file_iterator_filter_invalid_directory():
    with pytest.raises(FileNotFoundError):
        FileIterator("tests/data/invalid_dir_tree")

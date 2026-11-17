import pytest

from cli import CLI
from file_iterator import FileIterator


def test_file_iterator():
    cli = CLI(["tests/data/test_dir_tree", "tests/data/test_dir_tree"])
    file_iter = FileIterator(cli)
    files = list(file_iter.walk())
    assert len(files) == 10
    assert "tests/data/test_dir_tree/p2/p22/file22.ext2" in files


def test_file_iterator_filter():
    cli = CLI(["tests/data/test_dir_tree", "tests/data/test_dir_tree"])
    file_iter = FileIterator(cli)
    files = list(file_iter.filter_by_extension(["ext1"]).walk())
    assert len(files) == 4
    assert "tests/data/test_dir_tree/p1/p11/file11.ext1" in files
    assert "tests/data/test_dir_tree/p2/p22/file22.ext1" in files


def test_file_iterator_filter_invalid_directory():
    with pytest.raises(FileNotFoundError):
        FileIterator("tests/data/invalid_dir_tree")


def test_file_iterator_directory():
    file_iter = FileIterator("tests/data/test_dir_tree")

    assert file_iter.directory == "tests/data/test_dir_tree"


def test_file_iterator_custom_filter_chained_with_extension_filter():
    file_iter = FileIterator("tests/data/test_dir_tree")

    files = list(
        file_iter.filter_by_extension(["ext1"])
        .add_filter(lambda file: file.startswith("file2"))
        .walk()
    )

    assert sorted(files) == [
        "tests/data/test_dir_tree/p2/p21/file21.ext1",
        "tests/data/test_dir_tree/p2/p22/file22.ext1",
    ]


def test_file_iterator_filters_must_all_match():
    file_iter = FileIterator("tests/data/test_dir_tree")

    files = list(
        file_iter.add_filter(lambda file: file.endswith(".ext"))
        .add_filter(lambda file: False)
        .walk()
    )

    assert files == []

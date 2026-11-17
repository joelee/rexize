import os

import pytest

from cli import CLI

SOURCE_FOLDER = "tests/data/test_dir_tree"


@pytest.fixture(autouse=True)
def no_dev_mode(monkeypatch):
    monkeypatch.delenv("DEV_MODE", raising=False)


@pytest.fixture
def make_cli(tmp_path):
    def factory(*extra, debug_mode=False):
        args = [SOURCE_FOLDER, str(tmp_path / "out"), "-W", "50", *extra]
        return CLI(args, debug_mode=debug_mode)

    return factory


def test_print_writes_to_stdout(make_cli, capsys):
    make_cli().print("hello", "world")

    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
    assert captured.err == ""


def test_print_is_silent_with_quiet(make_cli, capsys):
    make_cli("--quiet").print("hello")

    assert capsys.readouterr().out == ""


def test_error_writes_to_stderr_even_with_quiet(make_cli, capsys):
    make_cli("--quiet").error("something failed")

    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "something failed\n"


def test_exception_writes_the_error_to_stderr(make_cli, capsys):
    make_cli().exception(ValueError("boom"))

    captured = capsys.readouterr()
    assert captured.err == "boom\n"
    assert captured.out == ""


def test_exception_also_prints_to_stdout_in_dev_mode(make_cli, capsys):
    make_cli(debug_mode=True).exception(ValueError("boom"))

    captured = capsys.readouterr()
    assert captured.err == "boom\n"
    assert "boom" in captured.out


def test_verbose_prints_only_with_the_flag(make_cli, capsys):
    make_cli().verbose("quiet detail")
    assert capsys.readouterr().out == ""

    make_cli("--verbose").verbose("loud detail")
    assert capsys.readouterr().out == "loud detail\n"


def test_debug_is_silent_by_default(make_cli, capsys):
    make_cli().debug("hidden")

    assert capsys.readouterr().out == ""


def test_debug_prints_in_debug_mode_and_dumps_the_parsed_args(make_cli, capsys):
    cli = make_cli(debug_mode=True)
    assert "Namespace" in capsys.readouterr().out  # parse_args prints the args

    cli.debug("shown")

    assert capsys.readouterr().out == "shown\n"


def test_debug_prints_with_the_dev_mode_environment_variable(
    make_cli, monkeypatch, capsys
):
    monkeypatch.setenv("DEV_MODE", "1")
    cli = make_cli()
    capsys.readouterr()

    cli.debug("from env")

    assert capsys.readouterr().out == "from env\n"


def test_exit_raises_system_exit_with_the_status(make_cli):
    cli = make_cli()

    with pytest.raises(SystemExit) as default:
        cli.exit()
    with pytest.raises(SystemExit) as custom:
        cli.exit(3)

    assert default.value.code == 0
    assert custom.value.code == 3


def test_args_default_to_the_tmp_folders_when_nothing_was_parsed():
    cli = CLI()

    args = cli.args

    assert args.input_folder == "/tmp"
    assert args.output_folder == "/tmp"
    assert cli.args is args  # parsed once, then reused


def test_validate_args_requires_an_input_folder(make_cli):
    cli = make_cli()
    cli.args.input_folder = ""

    with pytest.raises(ValueError, match="Input folder is required"):
        cli.validate_args()


def test_validate_args_requires_a_size(make_cli):
    cli = make_cli()
    cli.args.width = cli.args.height = cli.args.max_size = 0

    with pytest.raises(ValueError, match="At least one of width, height or max-size"):
        cli.validate_args()


def test_validate_args_defaults_the_output_folder_next_to_the_input(tmp_path):
    in_dir = tmp_path / "photos"
    in_dir.mkdir()
    cli = CLI([str(in_dir), str(tmp_path / "unused"), "-W", "50"])
    cli.args.output_folder = ""

    cli.validate_args()

    assert cli.args.output_folder == f"{in_dir}_resized"
    assert os.path.isdir(f"{in_dir}_resized")

import os
import shutil
import sys
from types import SimpleNamespace

import pytest

import main as rexize_main
from image import ImageFormat

SOURCE_IMAGE = "tests/data/test_img.png"  # PNG Image W 440 x H 578


def make_args(input_folder, output_folder, fmt=ImageFormat.WEBP):
    return SimpleNamespace(
        input_folder=str(input_folder),
        output_folder=str(output_folder),
        format=fmt,
    )


def run_main(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["rexize", *map(str, argv)])
    with pytest.raises(SystemExit) as exc:
        rexize_main.main()
    return exc.value.code


@pytest.fixture
def input_dir(tmp_path):
    folder = tmp_path / "in"
    folder.mkdir()
    shutil.copy(SOURCE_IMAGE, folder / "test_img.png")
    return folder


# get_output_file


def test_get_output_file_mirrors_the_input_tree(tmp_path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    source = in_dir / "a" / "b" / "photo.png"

    result = rexize_main.get_output_file(str(source), make_args(in_dir, out_dir))

    assert result == f"{out_dir}/a/b/photo.webp"


def test_get_output_file_creates_the_output_directory_tree(tmp_path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"
    source = in_dir / "a" / "b" / "photo.png"

    result = rexize_main.get_output_file(str(source), make_args(in_dir, out_dir))

    assert os.path.isdir(os.path.dirname(result))
    assert not os.path.exists(result)  # only the folders are created


def test_get_output_file_maps_jpeg_to_jpg(tmp_path):
    in_dir = tmp_path / "in"
    source = in_dir / "photo.png"

    result = rexize_main.get_output_file(
        str(source), make_args(in_dir, tmp_path / "out", ImageFormat.JPEG)
    )

    assert result.endswith("/photo.jpg")


@pytest.mark.parametrize(
    "fmt,extension",
    [
        (ImageFormat.PNG, "png"),
        (ImageFormat.GIF, "gif"),
        (ImageFormat.TIFF, "tiff"),
        (ImageFormat.BMP, "bmp"),
        (ImageFormat.WEBP, "webp"),
    ],
)
def test_get_output_file_uses_the_format_as_extension(tmp_path, fmt, extension):
    in_dir = tmp_path / "in"

    result = rexize_main.get_output_file(
        str(in_dir / "photo.gif"), make_args(in_dir, tmp_path / "out", fmt)
    )

    assert result.endswith(f"/photo.{extension}")


def test_get_output_file_strips_a_trailing_slash_from_the_output_folder(tmp_path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"

    result = rexize_main.get_output_file(
        str(in_dir / "photo.png"), make_args(in_dir, f"{out_dir}/")
    )

    assert result == f"{out_dir}/photo.webp"


def test_get_output_file_appends_the_extension_when_the_old_one_is_long(tmp_path):
    # Current behaviour: an existing extension of 5 or more characters (the dot
    # counts, so ".jpeg", ".tiff" and ".webp" too) is kept and the new one appended.
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"

    result = rexize_main.get_output_file(
        str(in_dir / "photo.jpeg"), make_args(in_dir, out_dir)
    )

    assert result == f"{out_dir}/photo.jpeg.webp"


def test_get_output_file_keeps_a_path_outside_the_input_folder(tmp_path):
    out_dir = tmp_path / "out"

    result = rexize_main.get_output_file("photo.png", make_args("elsewhere", out_dir))

    assert result == f"{out_dir}/photo.webp"


# main


def test_main_resizes_and_converts_an_image(monkeypatch, input_dir, tmp_path, capsys):
    out_dir = tmp_path / "out"

    code = run_main(monkeypatch, input_dir, out_dir, "-W", "50%", "-f", "png")

    assert code == 0
    assert (out_dir / "test_img.png").is_file()
    stdout = capsys.readouterr().out
    assert "Processed 1 files." in stdout
    assert f"{input_dir}/test_img.png --> {out_dir}/test_img.png" in stdout


def test_main_applies_rgb_and_grayscale(monkeypatch, input_dir, tmp_path):
    from PIL import Image

    out_dir = tmp_path / "out"

    code = run_main(
        monkeypatch, input_dir, out_dir, "-W", "100", "--rgb", "--grayscale", "-f", "png"
    )

    assert code == 0
    with Image.open(out_dir / "test_img.png") as result:
        assert result.mode == "L"
        assert result.width == 100


def test_main_applies_max_size(monkeypatch, input_dir, tmp_path):
    from PIL import Image

    out_dir = tmp_path / "out"

    code = run_main(monkeypatch, input_dir, out_dir, "-M", "200", "-f", "png")

    assert code == 0
    with Image.open(out_dir / "test_img.png") as result:
        assert max(result.size) == 200


def test_main_quiet_prints_nothing(monkeypatch, input_dir, tmp_path, capsys):
    code = run_main(monkeypatch, input_dir, tmp_path / "out", "-W", "50%", "-q")

    assert code == 0
    assert capsys.readouterr().out == ""


def test_main_skips_files_with_unsupported_extensions(monkeypatch, tmp_path, capsys):
    in_dir = tmp_path / "in"
    in_dir.mkdir()
    (in_dir / "notes.txt").write_text("not an image")

    code = run_main(monkeypatch, in_dir, tmp_path / "out", "-W", "50%")

    assert code == 0
    assert "Processed 0 files." in capsys.readouterr().out


def test_main_missing_input_folder_exits_55(monkeypatch, tmp_path, capsys):
    code = run_main(monkeypatch, tmp_path / "missing", tmp_path / "out", "-W", "50%")

    assert code == 55
    assert "Input folder not found or readable" in capsys.readouterr().err


def test_main_invalid_format_exits_55(monkeypatch, input_dir, tmp_path, capsys):
    code = run_main(monkeypatch, input_dir, tmp_path / "out", "-W", "50%", "-f", "xyz")

    assert code == 55
    assert "Invalid image format" in capsys.readouterr().err


def test_main_invalid_size_exits_55(monkeypatch, input_dir, tmp_path, capsys):
    code = run_main(monkeypatch, input_dir, tmp_path / "out", "-W", "abc")

    assert code == 55
    assert "Invalid value for ImageSizeUnit" in capsys.readouterr().err


def test_main_missing_positional_arguments_exit_2(monkeypatch):
    # argparse exits by itself, before main's own exit codes apply
    assert run_main(monkeypatch, "-W", "50%") == 2


@pytest.mark.xfail(
    strict=True,
    reason="validate_args tests `not width`, but the sizes are ImageSizeUnit "
    "objects (always truthy), so no size flag reaches the resize step and exits "
    "1 instead of the documented 55",
)
def test_main_without_a_size_exits_55(monkeypatch, input_dir, tmp_path):
    assert run_main(monkeypatch, input_dir, tmp_path / "out") == 55


def test_main_unreadable_image_exits_1(monkeypatch, tmp_path, capsys):
    in_dir = tmp_path / "in"
    in_dir.mkdir()
    (in_dir / "broken.png").write_text("this is not a PNG")

    code = run_main(monkeypatch, in_dir, tmp_path / "out", "-W", "50%")

    assert code == 1
    assert "cannot identify image file" in capsys.readouterr().err

from __future__ import annotations

import os
from io import StringIO
from typing import TYPE_CHECKING

import pytest

from xml_fmt.__main__ import run

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_mock import MockerFixture


@pytest.fixture
def min_xml_str() -> str:
    return "<?xml version='1.0' encoding='utf-8'?>\n<root />"


@pytest.fixture
def min_xml(tmp_path: Path, min_xml_str: str) -> Path:
    path = tmp_path / "name.xml"
    path.write_text(min_xml_str)
    return path


def test_xml_help(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as exc:
        run(["--help"])

    assert exc.value.code == 0

    out, err = capsys.readouterr()
    assert not err
    assert "XML (XSD)" in out


def test_xml_format_no_print_diff(capsys: pytest.CaptureFixture[str], tmp_path: Path, min_xml_str: str) -> None:
    xml = tmp_path / "name.xml"
    xml.write_text("<?xml version='1.0' encoding='utf-8'?>\n<root></root>\n")

    exit_code = run([str(xml), "--no-print-diff"])

    assert xml.read_text() == min_xml_str
    assert exit_code == 1

    out, err = capsys.readouterr()
    assert not err
    assert out.splitlines() == []


def test_xml_format_already_good(
    capsys: pytest.CaptureFixture[str], min_xml: Path, monkeypatch: pytest.MonkeyPatch, min_xml_str: str
) -> None:
    monkeypatch.setenv("NO_FMT", "1")

    exit_code = run([str(min_xml)])
    assert exit_code == 0

    assert min_xml.read_text() == min_xml_str

    out, err = capsys.readouterr()
    assert not err
    assert out.splitlines() == [f"no change for {min_xml}"]


def test_xml_stdin(capsys: pytest.CaptureFixture[str], mocker: MockerFixture, min_xml_str: str) -> None:
    mocker.patch("sys.stdin", StringIO("<?xml version='1.0' encoding='utf-8'?>\n<root></root>\n"))

    exit_code = run(["-"])
    assert exit_code == 1

    out, err = capsys.readouterr()
    assert not err
    assert out == min_xml_str


def test_xml_path_missing(capsys: pytest.CaptureFixture[str], tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_path)

    with pytest.raises(SystemExit):
        run(["demo.xml"])

    out, err = capsys.readouterr()
    assert "\nxml-fmt: error: argument inputs: path does not exist\n" in err
    assert not out


def test_xml_path_is_folder(capsys: pytest.CaptureFixture[str], tmp_path: Path) -> None:
    path = tmp_path / "demo.xml"
    os.mkfifo(path)

    with pytest.raises(SystemExit):
        run([str(path)])

    out, err = capsys.readouterr()
    assert "\nxml-fmt: error: argument inputs: path is not a file\n" in err
    assert not out


def test_xml_path_no_read(capsys: pytest.CaptureFixture[str], min_xml: Path) -> None:
    start = min_xml.stat().st_mode
    min_xml.chmod(0o000)

    try:
        with pytest.raises(SystemExit):
            run([str(min_xml)])
    finally:
        min_xml.chmod(start)

    out, err = capsys.readouterr()
    assert "\nxml-fmt: error: argument inputs: cannot read path\n" in err
    assert not out


def test_xml_path_no_write(capsys: pytest.CaptureFixture[str], min_xml: Path) -> None:
    start = min_xml.stat().st_mode
    min_xml.chmod(0o400)

    try:
        with pytest.raises(SystemExit):
            run([str(min_xml)])
    finally:
        min_xml.chmod(start)

    out, err = capsys.readouterr()
    assert "\nxml-fmt: error: argument inputs: cannot write path\n" in err
    assert not out


def test_xml_format_add_newline(capsys: pytest.CaptureFixture[str], tmp_path: Path, min_xml_str: str) -> None:
    xml = tmp_path / "name.xml"
    xml.write_text(min_xml_str)

    exit_code = run([str(xml), "--no-print-diff", "--add-eof-newline"])

    assert xml.read_text() == min_xml_str + "\n"
    assert exit_code == 1

    out, err = capsys.readouterr()
    assert not err
    assert out.splitlines() == []

"""Format XMLs."""

from __future__ import annotations

import os
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser, ArgumentTypeError, Namespace
from difflib import unified_diff
from importlib.metadata import version
from pathlib import Path
from typing import TYPE_CHECKING
from xml.etree.ElementTree import XML, indent, tostring  # noqa: S405

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence


class Options(Namespace):
    """Options for pyproject-fmt tool."""

    inputs: list[Path | None]
    stdout: bool
    check: bool
    no_print_diff: bool

    indent: str
    expand_empty_elements: bool
    add_eof_newline: bool


def run(args: Sequence[str] | None = None) -> int:
    """
    Run the formatter.

    :param args: command line arguments, by default use sys.argv[1:]
    :return: exit code - 0 means already formatted correctly, otherwise 1
    """  # noqa: DOC201
    parser = _build_cli()
    opts = Options()
    parser.parse_args(args=args, namespace=opts)
    results = [_handle_one(filename, opts) for filename in opts.inputs]
    return 1 if any(results) else 0  # exit with non success on change


class _Formatter(ArgumentDefaultsHelpFormatter):
    def __init__(self, prog: str) -> None:
        super().__init__(prog, max_help_position=29, width=240)


def _build_cli() -> ArgumentParser:
    parser = ArgumentParser(formatter_class=_Formatter, prog="xml-fmt")
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        help="version of the project",
        version=f"%(prog)s ({version('xml-fmt')})",
    )

    mode_group = parser.add_argument_group("run mode")
    mode = mode_group.add_mutually_exclusive_group()
    msg = "print the formatted XML to the stdout, implied if reading from stdin"
    mode.add_argument("-s", "--stdout", action="store_true", help=msg)
    msg = "check and fail if any input would be formatted, printing any diffs"
    mode.add_argument("--check", action="store_true", help=msg)
    mode_group.add_argument(
        "-n",
        "--no-print-diff",
        action="store_true",
        help="controls if to print diff - when running in check mode",
    )

    format_group = parser.add_argument_group("formatting behavior")
    format_group.add_argument("--indent", default="  ", help="indentation characters to use - two space by default")
    format_group.add_argument(
        "--expand-empty-elements",
        action="store_true",
        help="controls if empty XML elements should be collapsed into a self closing element or expanded",
    )
    format_group.add_argument(
        "-N",
        "--add-eof-newline",
        action="store_true",
        help="controls if a trailing newline is appended to the output",
    )

    msg = "XML (XSD) file(s) to format, use '-' to read from stdin"
    parser.add_argument("inputs", nargs="+", type=_path_creator, help=msg)
    return parser


def _path_creator(argument: str) -> Path | None:
    if argument == "-":
        return None  # stdin, no further validation needed
    path = Path(argument).absolute()
    if not path.exists():
        msg = "path does not exist"
        raise ArgumentTypeError(msg)
    if not path.is_file():
        msg = "path is not a file"
        raise ArgumentTypeError(msg)
    if not os.access(path, os.R_OK):
        msg = "cannot read path"
        raise ArgumentTypeError(msg)
    if not os.access(path, os.W_OK):
        msg = "cannot write path"
        raise ArgumentTypeError(msg)
    return path


def _handle_one(filename: Path | None, opts: Options) -> bool:
    before = sys.stdin.read() if filename is None else filename.read_text(encoding="utf-8")
    formatted = _format(before, opts)

    changed = before != formatted
    if filename is None or opts.stdout:  # when reading from stdin or writing to stdout, print new format
        print(formatted, end="")  # noqa: T201
        return changed

    if before != formatted and not opts.check:
        filename.write_text(formatted, encoding="utf-8")
    if opts.no_print_diff:
        return changed
    try:
        name = str(filename.relative_to(Path.cwd()))
    except ValueError:
        name = str(filename)
    diff: Iterable[str] = []
    if changed:
        diff = unified_diff(before.splitlines(), formatted.splitlines(), fromfile=name, tofile=name)

    if diff:
        diff = _color_diff(diff)
        print("\n".join(diff))  # print diff on change  # noqa: T201
    else:
        print(f"no change for {name}")  # noqa: T201
    return changed


def _format(raw: str, opts: Options) -> str:
    element = XML(raw)
    indent(element, opts.indent)
    return (
        tostring(
            element,
            encoding="unicode",
            xml_declaration=True,
            short_empty_elements=not opts.expand_empty_elements,
        )
        + "\n" * opts.add_eof_newline
    )


GREEN = "\u001b[32m"
RED = "\u001b[31m"
RESET = "\u001b[0m"


def _color_diff(diff: Iterable[str]) -> Iterable[str]:
    for line in diff:
        if line.startswith("+"):
            yield f"{GREEN}{line}{RESET}"
        elif line.startswith("-"):
            yield f"{RED}{line}{RESET}"
        else:
            yield line


if __name__ == "__main__":
    raise SystemExit(run(sys.argv[1:]))

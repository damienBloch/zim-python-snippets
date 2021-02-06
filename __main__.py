#!/usr/bin/env python3
import argparse
import os
import re
from contextlib import contextmanager
from typing import Iterable


@contextmanager
def working_directory(dir: str):
    prev_wd = os.getcwd()
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(prev_wd)


def parse_page_info():
    parser = argparse.ArgumentParser(description="Run python snippets "
                                                 "inside a zim file")
    parser.add_argument('attachment_dir', type=str,
                        help="attachment directory of the current dir")
    parser.add_argument('page_path', type=str,
                        help="dir to the page file")
    return parser.parse_args()


def load_page(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()


def extract_snippets(text: str) -> Iterable[str]:
    pattern = r"{{{code: (?P<args>.*)\s(?P<code>(?:.|\s)*?)}}}"
    for match in re.finditer(pattern, text):
        lang_pattern = r"lang=\"(?:python|python3)\""
        if re.match(lang_pattern, match.group('args')):
            yield match.group('code')


if __name__ == '__main__':
    args = parse_page_info()
    page_text = load_page(args.page_path)
    for code in extract_snippets(page_text):
        with working_directory(args.attachment_dir):
            exec(code, {})
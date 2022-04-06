"""Do an integration test. Only use simple html files."""

import json
import os
import subprocess

HTML_TEST_FILES = os.path.abspath(os.path.dirname(__file__))


def test_valid():
    """Command line test for valid files"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/']) == 0


def test_invalid():
    """Command line test for invalid files"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/invalid/']) == 1


def test_invalid_with_css():
    """Command line test for invalid CSS and HTML"""
    assert subprocess.call([
        'html5validator',
        f'--root={HTML_TEST_FILES}/invalid/',
        '--also-check-css',
    ]) == 2


def test_invalid_css_only():
    """Command line test for invalid CSS only"""
    assert subprocess.call([
        'html5validator',
        '--root', f'{HTML_TEST_FILES}/invalid/',
        '--skip-non-css',
    ]) == 1


def test_invalid_single_file():
    """Command line test for invalid single file"""
    assert subprocess.call([
        'html5validator',
        f'{HTML_TEST_FILES}/invalid/index.html',
    ]) == 1


def test_warning():
    """Command line test for warnings"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/warning/',
                            '--show-warnings']) == 1


def test_warning_but_pass():
    """Command line test for passing warnings"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/warning/']) == 0


def test_return_value():
    """Command line test for error code return value"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/return_value/',
                            '--match=254.html']) == 254
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/return_value/',
                            '--match=255.html']) == 255
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/return_value/',
                            '--match=256.html']) == 255


def test_angularjs():
    """Command line test for angularjs"""
    assert subprocess.call([
        'html5validator',
        f'--root={HTML_TEST_FILES}/angularjs/',
        '--ignore-re=Attribute “ng-[a-z-]+” not allowed',
    ]) == 0


def test_angularjs_no_output_with_ignore():
    """Make sure there is no spurious output when messages are ignored."""

    output = subprocess.check_output([
        'html5validator',
        f'--root={HTML_TEST_FILES}/angularjs/',
        '--ignore-re=Attribute “ng-[a-z-]+” not allowed',
    ])
    assert output == b''


def test_angularjs_normal_quotes():
    """Command line test for passing angularjs"""
    assert subprocess.call([
        'html5validator',
        f'--root={HTML_TEST_FILES}/angularjs/',
        '--ignore-re=Attribute "ng-[a-z-]+" not allowed',
    ]) == 0


def test_multiple_ignoreres():
    """Command line test for multiple regex ignores"""
    assert subprocess.call([
        'html5validator',
        f'--root={HTML_TEST_FILES}/multiple_ignores/',
        '--ignore-re', 'Attribute “ng-[a-z-]+” not allowed',
        'Start tag seen without seeing a doctype first',
    ]) == 0


def test_ignore_and_ignorere():
    """Command line test for ignore and regex ignores"""
    assert subprocess.call([
        'html5validator',
        f'--root={HTML_TEST_FILES}/multiple_ignores/',
        '--ignore-re', 'Attribute “ng-[a-z-]+” not allowed',
        '--ignore', 'Start tag seen without seeing a doctype first',
    ]) == 0


def test_stack_size():
    """Command line test for stack size"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/',
                            '-lll']) == 0


def test_valid_format_flags():
    """Command line test for output format for valid files"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/',
                            '--format', 'text']) == 0
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/',
                            '--format', 'gnu']) == 0
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/',
                            '--format', 'json']) == 0
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/',
                            '--format', 'xml']) == 0


def test_invalid_format_flags():
    """Command line test for output format for invalid files"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/invalid/',
                            '--format', 'text']) == 3
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/invalid/',
                            '--format', 'gnu']) == 1
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/invalid/',
                            '--format', 'json']) == 1
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/invalid/',
                            '--format', 'xml']) == 8


def test_json_parseable():
    out = subprocess.run(['html5validator',
                          f'--root={HTML_TEST_FILES}/invalid/',
                          '--format=json'], stdout=subprocess.PIPE).stdout
    assert out
    for line in out.decode('utf-8').splitlines():
        print(line)
        json.loads(line)


def test_log_file():
    """Command line test for log file"""
    assert subprocess.call(['html5validator',
                            f'--root={HTML_TEST_FILES}/valid/',
                            '--log-file', 'test_command_line',
                            '--log', 'DEBUG']) == 0


def test_skip():
    """Command line test for skipping file"""
    assert subprocess.call(['html5validator',
                            '--blacklist', 'index.html',
                            '--also-check-css',
                            f'--root={HTML_TEST_FILES}/invalid/'
                            ]) == 1


if __name__ == '__main__':
    test_valid()
    test_invalid()
    test_return_value()
    test_angularjs()
    test_multiple_ignoreres()
    test_ignore_and_ignorere()
    test_stack_size()
    test_valid_format_flags()
    test_invalid_format_flags()
    test_log_file()
    test_skip()

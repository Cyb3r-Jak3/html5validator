# -*- coding: utf-8 -*-
"""Do an integration test for config file usage."""

import os
import subprocess

HTML_TEST_FILES = os.path.abspath(os.path.dirname(__file__))


def test_no_java():
    """Test for no java install"""
    old_path = os.environ["PATH"]
    old_path.replace("/usr/bin", "")
    print(old_path)
    os.environ["PATH"] = old_path
    print(subprocess.call(["which", "java"]))
    out = subprocess.call(['html5validator',
                            '--root={}/valid/'.format(HTML_TEST_FILES)])
    print(out)
    os.environ["PATH"] = old_path

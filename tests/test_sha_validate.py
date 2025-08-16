"""Do an integration test. Only use simple html files."""

import subprocess

def test_hash():
    """Test for checking the hash of vnu.jar"""
    assert subprocess.call([
        "html5validator", "--check-hash",
    ]) == 0


def test_sha_hash_mismatch(tmp_path):
    jar_path = tmp_path / "vnu.jar"
    sha1_path = tmp_path / "vnu.jar.sha1"
    jar_path.write_bytes(b"dummy content")
    sha1_path.write_text("incorrecthash")

    # Patch __file__ to simulate location
    import vnujar
    old_file = vnujar.__file__
    vnujar.__file__ = str(tmp_path / "__init__.py")

    try:
        result = vnujar.check_sha_hash()
        assert result is False
    finally:
        vnujar.__file__ = old_file
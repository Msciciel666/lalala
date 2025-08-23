import runpy
import sys
import types
from unittest import mock
import pytest

class DummyTags:
    def __init__(self):
        self.deleted = False
        self.saved = False

    def delete(self):
        self.deleted = True

    def save(self, fname):
        self.saved = True
        self.fname = fname


def test_no_id3_header(capsys):
    fake_mod = types.SimpleNamespace(
        ID3=lambda f: (_ for _ in ()).throw(Exception()),
        ID3NoHeaderError=Exception,
    )
    with mock.patch.dict(sys.modules, {"mutagen.id3": fake_mod, "mutagen": types.SimpleNamespace(id3=fake_mod)}):
        runpy.run_path('oczyszczanie_exif.py')
    captured = capsys.readouterr()
    assert 'Brak tagów ID3' in captured.out


def test_delete_tags(capsys):
    tags = DummyTags()
    fake_mod = types.SimpleNamespace(ID3=lambda f: tags, ID3NoHeaderError=Exception)
    with mock.patch.dict(sys.modules, {"mutagen.id3": fake_mod, "mutagen": types.SimpleNamespace(id3=fake_mod)}):
        runpy.run_path('oczyszczanie_exif.py')
    assert tags.deleted
    assert tags.saved
    captured = capsys.readouterr()
    assert 'Usunięto tagi ID3.' in captured.out
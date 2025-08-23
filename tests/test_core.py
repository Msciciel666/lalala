from types import SimpleNamespace
from core import main


def test_cli_crawl(monkeypatch, capsys):
    """Verify crawl subcommand triggers plugin scan."""
    called = {}

    def fake_scan(text):
        called["text"] = text
        return []

    monkeypatch.setattr(
        main.loader,
        "load_plugins",
        lambda: {"plugin_sample": SimpleNamespace(scan=fake_scan)},
    )
    main.main(["crawl", "example.com"])
    captured = capsys.readouterr()
    assert "Crawling http://example.com" in captured.out
    assert called["text"] == "http://example.com"


def test_cli_parse_dump(tmp_path, monkeypatch, capsys):
    """Verify parse-dump subcommand scans file content."""
    dump = tmp_path / "dump.txt"
    dump.write_text("password=secret")
    called = {}

    def fake_scan(text):
        called["text"] = text
        return ["secret"]

    monkeypatch.setattr(
        main.loader,
        "load_plugins",
        lambda: {"plugin_credentials": SimpleNamespace(scan=fake_scan)},
    )
    main.main(["parse-dump", str(dump)])
    captured = capsys.readouterr()
     assert "Parsing" in captured.out
    assert called["text"] == "password=secret"

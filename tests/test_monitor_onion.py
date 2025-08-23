import runpy
import sys
from unittest import mock
import pytest


def test_no_arguments(capsys):
    argv = ["monitor_onion.py"]
    with mock.patch.dict(sys.modules, {"requests": mock.Mock()}):
        with mock.patch.object(sys, "argv", argv):
            with pytest.raises(SystemExit):
                runpy.run_path("monitor_onion.py")
    captured = capsys.readouterr()
    assert "Podaj co najmniej jeden URL .onion" in captured.out


def test_single_url(monkeypatch, capsys):
    argv = ["monitor_onion.py", "http://example.onion"]
    called = {}

    class DummyResponse:
        status_code = 200

    def fake_get(url, proxies=None, timeout=None):
        called["url"] = url
        called["proxies"] = proxies
        called["timeout"] = timeout
        return DummyResponse()

    def fake_sleep(_):
        raise RuntimeError("stop")

    monkeypatch.setattr(sys, "argv", argv)
    with mock.patch.dict(sys.modules, {"requests": mock.Mock(get=fake_get)}):
        monkeypatch.setattr("time.sleep", fake_sleep)
        with pytest.raises(RuntimeError):
            runpy.run_path("monitor_onion.py")

    assert called["url"] == "http://example.onion"
    assert called["proxies"] == {
        "http": "socks5h://127.0.0.1:9150",
        "https": "socks5h://127.0.0.1:9150",
    }
    assert called["timeout"] == 15
    captured = capsys.readouterr()
    assert "OK" in captured.out
    assert "200" in captured.out
from scanner import plugin_email, plugin_credentials


def test_email_scan():
    """plugin_email should detect email addresses."""
    text = "contact: user@example.com"
    matches = plugin_email.scan(text)
    assert matches == ["user@example.com"]


def test_credentials_scan():
    """plugin_credentials should detect password patterns."""
    text = "password=secret"
    matches = plugin_credentials.scan(text)
    assert matches == ["secret"]
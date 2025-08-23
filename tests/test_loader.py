from scanner import loader


def test_plugin_loaded():
    """Ensure plugins are loaded by the loader."""
    plugins = loader.load_plugins()
    assert "plugin_sample" in plugins
 assert "plugin_email" in plugins
    assert "plugin_credentials" in plugins

import pytest


class TestValidate:
    def test_missing_vars(self, monkeypatch):
        monkeypatch.setattr("nube_agent.config.OPENAI_API_KEY", "")
        monkeypatch.setattr("nube_agent.config.TIENDANUBE_ACCESS_TOKEN", "")
        monkeypatch.setattr("nube_agent.config.TIENDANUBE_STORE_ID", "")
        from nube_agent.config import validate
        with pytest.raises(SystemExit, match="OPENAI_API_KEY"):
            validate()

    def test_all_present(self, monkeypatch):
        monkeypatch.setattr("nube_agent.config.OPENAI_API_KEY", "sk-test")
        monkeypatch.setattr("nube_agent.config.TIENDANUBE_ACCESS_TOKEN", "tok")
        monkeypatch.setattr("nube_agent.config.TIENDANUBE_STORE_ID", "123")
        from nube_agent.config import validate
        validate()  # Should not raise

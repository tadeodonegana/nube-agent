from nube_agent.agent import build_agent


class TestBuildAgent:
    def test_returns_runnable(self):
        agent = build_agent()
        # The agent should be a compiled state graph with an invoke method
        assert callable(getattr(agent, "invoke", None))
        assert callable(getattr(agent, "stream", None))

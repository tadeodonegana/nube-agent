from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, StateBackend, StoreBackend
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore

from nube_agent.config import MODEL
from nube_agent.prompts import load_system_prompt
from nube_agent.subagents import SUBAGENTS
from nube_agent.tools.store import get_store_info

DESTRUCTIVE_TOOLS = {
    "delete_product",
    "delete_category",
    "delete_variant",
    "delete_image",
    "cancel_order",
    "delete_coupon",
    "delete_page",
}


def _make_backend(runtime):
    """Create a CompositeBackend that routes /memories/ to the store."""
    return CompositeBackend(
        default=StateBackend(runtime),
        routes={"/memories/": StoreBackend(runtime)},
    )


def build_agent():
    """Create and return the deep agent with sub-agents, HITL, and memory.

    Both the store and checkpointer are in-memory: all state and memories are
    lost when the CLI process exits.  See "What's Next" in the blog post for
    the plan to swap these for persistent backends.
    """
    store = InMemoryStore()
    checkpointer = MemorySaver()
    agent = create_deep_agent(
        model=MODEL,
        tools=[get_store_info],
        system_prompt=load_system_prompt(),
        skills=["skills/store-overview/"],
        subagents=SUBAGENTS,
        backend=_make_backend,
        store=store,
        checkpointer=checkpointer,
        interrupt_on={name: True for name in DESTRUCTIVE_TOOLS},
    )
    return agent

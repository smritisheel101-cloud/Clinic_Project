"""
 Memory Configuration file. This file is for  memory configuration

"""

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

#short term memory configuration
checkpointer = InMemorySaver()

#long term memory configuration
store= InMemoryStore()
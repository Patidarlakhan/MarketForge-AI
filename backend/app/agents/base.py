"""
AI Marketing Content Engine — Base Agent

Abstract base class for all AI agents in the system.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.llm import LLMProvider, get_llm_provider


class BaseAgent(ABC):
    """Abstract base agent providing LLM execution capabilities."""

    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        self.llm = llm_provider or get_llm_provider()

    @abstractmethod
    async def run(self, *args, **kwargs):
        """Execute agent task."""
        pass

"""
Base agent class for the BD Automation pipeline.

All agents inherit from BaseAgent and implement:
  - run(): core agent logic
  - validate_input(): input schema validation
  - validate_output(): output schema validation

Each agent is configured with:
  - model: OpenRouter model identifier (per-agent routing)
  - temperature: sampling temperature
  - max_retries: retry count on failure
  - prompt_template: path to the .md prompt template
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for an agent instance."""

    name: str
    model: str  # OpenRouter model ID, e.g. "anthropic/claude-sonnet-4-20250514"
    temperature: float = 0.3
    max_tokens: int = 4096
    max_retries: int = 2
    prompt_template: str = ""  # Relative path under prompts/
    timeout_seconds: int = 60


@dataclass
class AgentResult:
    """Standardized output from any agent run."""

    agent_name: str
    status: str  # "success" | "error" | "retry"
    data: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "status": self.status,
            "data": self.data,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
            "errors": self.errors,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, default=str)


class BaseAgent(ABC):
    """Abstract base class for all BD Automation agents."""

    def __init__(self, config: AgentConfig) -> None:
        self.config = config
        self.logger = logging.getLogger(f"agents.{config.name}")

    @abstractmethod
    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """Execute the agent's core logic."""
        ...

    @abstractmethod
    def validate_input(self, input_data: dict[str, Any]) -> bool:
        """Validate input data against the agent's expected schema."""
        ...

    @abstractmethod
    def validate_output(self, result: AgentResult) -> bool:
        """Validate output data meets downstream requirements."""
        ...

    def load_prompt(self) -> str:
        """Load the prompt template from the prompts/ directory."""
        if not self.config.prompt_template:
            raise ValueError(f"No prompt template configured for {self.config.name}")

        prompt_path = Path("prompts") / self.config.prompt_template
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_path}")

        return prompt_path.read_text(encoding="utf-8")

    def _build_checkpoint(self, input_data: dict, result: AgentResult) -> dict:
        """Build a checkpoint record for the pipeline log."""
        return {
            "agent": self.config.name,
            "model": self.config.model,
            "timestamp": result.timestamp,
            "status": result.status,
            "input_keys": list(input_data.keys()),
            "output_keys": list(result.data.keys()),
            "errors": result.errors,
        }

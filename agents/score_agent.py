"""
Score Agent — Pipeline Stage 2
===============================
Purpose: Deep multi-dimensional scoring of filtered offer-profile pairs.
Model strategy: Strong reasoning model (e.g., anthropic/claude-sonnet-4-20250514)
Input: Filtered offer-profile pair + empathy map + signals
Output: Numeric scores per dimension + composite score + reasoning

Scoring dimensions:
  1. Industry Alignment (0-100)
  2. Technical Fit (0-100)
  3. Budget Signals (0-100)
  4. Timing/Urgency (0-100)
  5. Relationship Proximity (0-100)
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentConfig, AgentResult, BaseAgent

SCORING_DIMENSIONS = [
    "industry_alignment",
    "technical_fit",
    "budget_signals",
    "timing_urgency",
    "relationship_proximity",
]

DEFAULT_CONFIG = AgentConfig(
    name="score",
    model="anthropic/claude-sonnet-4-20250514",
    temperature=0.2,
    max_tokens=4096,
    max_retries=2,
    prompt_template="score_agent.md",
    timeout_seconds=60,
)


class ScoreAgent(BaseAgent):
    """Performs deep multi-dimensional scoring on filtered pairs."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        super().__init__(config or DEFAULT_CONFIG)

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """
        Score a filtered offer-profile pair across multiple dimensions.

        Input schema:
            {
                "offer": { ... },
                "profile": { ... },
                "empathy_map": { ... } | null,
                "signals": [ ... ],
                "filter_result": { "pass": true, "rationale": str }
            }

        Output schema:
            {
                "offer_id": str,
                "profile_id": str,
                "scores": {
                    "industry_alignment": int (0-100),
                    "technical_fit": int (0-100),
                    "budget_signals": int (0-100),
                    "timing_urgency": int (0-100),
                    "relationship_proximity": int (0-100)
                },
                "composite_score": float (0-100),
                "reasoning": str,
                "key_strengths": [str],
                "key_risks": [str]
            }
        """
        if not self.validate_input(input_data):
            return AgentResult(
                agent_name=self.config.name,
                status="error",
                errors=["Invalid input: missing offer, profile, or filter_result"],
            )

        prompt = self.load_prompt()

        # TODO: Replace with actual OpenRouter API call
        self.logger.info(
            "Scoring: offer=%s profile=%s",
            input_data["offer"].get("id"),
            input_data["profile"].get("id"),
        )

        result = AgentResult(
            agent_name=self.config.name,
            status="success",
            data={
                "offer_id": input_data["offer"].get("id", ""),
                "profile_id": input_data["profile"].get("id", ""),
                "scores": {dim: 0 for dim in SCORING_DIMENSIONS},
                "composite_score": 0.0,
                "reasoning": "Placeholder — implement LLM call",
                "key_strengths": [],
                "key_risks": [],
            },
            metadata={"model": self.config.model, "dimensions": SCORING_DIMENSIONS},
        )

        if not self.validate_output(result):
            result.status = "error"
            result.errors.append("Output validation failed")

        return result

    def validate_input(self, input_data: dict[str, Any]) -> bool:
        return (
            isinstance(input_data, dict)
            and "offer" in input_data
            and "profile" in input_data
            and "filter_result" in input_data
            and input_data.get("filter_result", {}).get("pass") is True
        )

    def validate_output(self, result: AgentResult) -> bool:
        if result.status != "success":
            return False
        data = result.data
        required = {"offer_id", "profile_id", "scores", "composite_score", "reasoning"}
        if not required.issubset(data.keys()):
            return False
        scores = data.get("scores", {})
        return all(dim in scores for dim in SCORING_DIMENSIONS)

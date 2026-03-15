"""
Critic Agent — Pipeline Stage 3
=================================
Purpose: Validates scoring reasoning, detects hallucinations, ensures quality.
Model strategy: Strong reasoning model (e.g., anthropic/claude-sonnet-4-20250514)
Input: Score agent output + original data
Output: Validation verdict + corrections + retry signal

Architecture decision: Critic is MANDATORY — cannot be skipped.
Max retries: 2 (if critic rejects, score agent re-runs with feedback).
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentConfig, AgentResult, BaseAgent

DEFAULT_CONFIG = AgentConfig(
    name="critic",
    model="anthropic/claude-sonnet-4-20250514",
    temperature=0.1,  # Low temp for consistent evaluation
    max_tokens=4096,
    max_retries=2,
    prompt_template="critic_agent.md",
    timeout_seconds=60,
)

# Maximum times the Score→Critic loop can retry
MAX_CRITIC_RETRIES = 2


class CriticAgent(BaseAgent):
    """Validates scoring output for quality, consistency, and hallucinations."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        super().__init__(config or DEFAULT_CONFIG)

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """
        Validate and critique the Score agent's output.

        Input schema:
            {
                "offer": { ... },
                "profile": { ... },
                "score_result": {
                    "scores": { ... },
                    "composite_score": float,
                    "reasoning": str,
                    "key_strengths": [str],
                    "key_risks": [str]
                },
                "retry_count": int (0-based)
            }

        Output schema:
            {
                "verdict": "approved" | "rejected" | "adjusted",
                "issues_found": [
                    {
                        "type": "hallucination" | "inconsistency" | "unsupported_claim" | "missing_evidence",
                        "description": str,
                        "affected_dimension": str | null,
                        "severity": "low" | "medium" | "high"
                    }
                ],
                "adjusted_scores": { ... } | null,
                "adjusted_composite": float | null,
                "feedback_for_retry": str | null,
                "should_retry": bool,
                "quality_score": float (0-1)
            }
        """
        if not self.validate_input(input_data):
            return AgentResult(
                agent_name=self.config.name,
                status="error",
                errors=["Invalid input: missing score_result or original data"],
            )

        retry_count = input_data.get("retry_count", 0)
        if retry_count >= MAX_CRITIC_RETRIES:
            self.logger.warning(
                "Max critic retries reached (%d). Forcing approval with low quality.",
                retry_count,
            )

        prompt = self.load_prompt()

        # TODO: Replace with actual OpenRouter API call
        self.logger.info(
            "Critic evaluating: offer=%s profile=%s (retry=%d)",
            input_data["offer"].get("id"),
            input_data["profile"].get("id"),
            retry_count,
        )

        result = AgentResult(
            agent_name=self.config.name,
            status="success",
            data={
                "verdict": "approved",
                "issues_found": [],
                "adjusted_scores": None,
                "adjusted_composite": None,
                "feedback_for_retry": None,
                "should_retry": False,
                "quality_score": 0.0,
            },
            metadata={
                "model": self.config.model,
                "retry_count": retry_count,
                "max_retries": MAX_CRITIC_RETRIES,
            },
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
            and "score_result" in input_data
            and isinstance(input_data["score_result"], dict)
        )

    def validate_output(self, result: AgentResult) -> bool:
        if result.status != "success":
            return False
        data = result.data
        required = {"verdict", "issues_found", "should_retry", "quality_score"}
        if not required.issubset(data.keys()):
            return False
        return data["verdict"] in ("approved", "rejected", "adjusted")

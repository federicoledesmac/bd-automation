"""
Filter Agent — Pipeline Stage 1
================================
Purpose: Fast pre-filtering of offer-profile pairs using cheap/fast LLM.
Model strategy: Fast, low-cost model (e.g., mistral/mistral-small)
Input: Raw offer + profile data
Output: Boolean pass/fail with brief rationale

This agent reduces the candidate pool before expensive scoring.
Only pairs that pass the filter proceed to the Score agent.
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentConfig, AgentResult, BaseAgent

DEFAULT_CONFIG = AgentConfig(
    name="filter",
    model="mistralai/mistral-small-latest",
    temperature=0.1,
    max_tokens=1024,
    max_retries=1,
    prompt_template="filter_agent.md",
    timeout_seconds=30,
)


class FilterAgent(BaseAgent):
    """Pre-filters offer-profile pairs for relevance."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        super().__init__(config or DEFAULT_CONFIG)

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """
        Evaluate whether a profile is a plausible match for an offer.

        Input schema:
            {
                "offer": { "id", "title", "services", "verticals", "tech_stack" },
                "profile": { "id", "company", "industry", "signals", "tech_used" }
            }

        Output schema:
            {
                "pass": bool,
                "rationale": str,
                "confidence": float (0-1),
                "offer_id": str,
                "profile_id": str
            }
        """
        if not self.validate_input(input_data):
            return AgentResult(
                agent_name=self.config.name,
                status="error",
                errors=["Invalid input: missing required fields (offer, profile)"],
            )

        prompt = self.load_prompt()

        # TODO: Replace with actual OpenRouter API call
        # response = await openrouter_client.chat(
        #     model=self.config.model,
        #     messages=[
        #         {"role": "system", "content": prompt},
        #         {"role": "user", "content": json.dumps(input_data)},
        #     ],
        #     temperature=self.config.temperature,
        #     max_tokens=self.config.max_tokens,
        # )

        self.logger.info(
            "Filter evaluated: offer=%s profile=%s",
            input_data["offer"].get("id"),
            input_data["profile"].get("id"),
        )

        # Placeholder result
        result = AgentResult(
            agent_name=self.config.name,
            status="success",
            data={
                "pass": True,
                "rationale": "Placeholder — implement LLM call",
                "confidence": 0.0,
                "offer_id": input_data["offer"].get("id", ""),
                "profile_id": input_data["profile"].get("id", ""),
            },
            metadata={"model": self.config.model},
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
            and isinstance(input_data["offer"], dict)
            and isinstance(input_data["profile"], dict)
        )

    def validate_output(self, result: AgentResult) -> bool:
        required_keys = {"pass", "rationale", "confidence", "offer_id", "profile_id"}
        return result.status == "success" and required_keys.issubset(
            result.data.keys()
        )

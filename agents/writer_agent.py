"""
Writer Agent — Pipeline Stage 4
=================================
Purpose: Generate personalized outreach content for approved matches.
Model strategy: Creative model (e.g., openai/gpt-4o or anthropic/claude-sonnet)
Input: Approved & scored match with critic validation
Output: Personalized outreach message(s) + subject lines + channel recommendations

Only processes matches that passed the Critic stage.
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentConfig, AgentResult, BaseAgent

DEFAULT_CONFIG = AgentConfig(
    name="writer",
    model="openai/gpt-4o",
    temperature=0.7,  # Higher temp for creative output
    max_tokens=4096,
    max_retries=1,
    prompt_template="writer_agent.md",
    timeout_seconds=60,
)


class WriterAgent(BaseAgent):
    """Generates personalized outreach content for approved matches."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        super().__init__(config or DEFAULT_CONFIG)

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """
        Generate outreach content for an approved match.

        Input schema:
            {
                "offer": { ... },
                "profile": { ... },
                "score_result": { "scores", "composite_score", "key_strengths", "key_risks" },
                "critic_result": { "verdict": "approved", "quality_score" },
                "empathy_map": { ... } | null
            }

        Output schema:
            {
                "offer_id": str,
                "profile_id": str,
                "outreach_variants": [
                    {
                        "channel": "email" | "linkedin" | "twitter",
                        "subject": str | null,
                        "body": str,
                        "tone": "formal" | "casual" | "technical",
                        "personalization_hooks": [str]
                    }
                ],
                "talking_points": [str],
                "recommended_channel": str,
                "follow_up_timing": str
            }
        """
        if not self.validate_input(input_data):
            return AgentResult(
                agent_name=self.config.name,
                status="error",
                errors=["Invalid input: critic must approve before writing"],
            )

        prompt = self.load_prompt()

        # TODO: Replace with actual OpenRouter API call
        self.logger.info(
            "Writer generating outreach: offer=%s profile=%s",
            input_data["offer"].get("id"),
            input_data["profile"].get("id"),
        )

        result = AgentResult(
            agent_name=self.config.name,
            status="success",
            data={
                "offer_id": input_data["offer"].get("id", ""),
                "profile_id": input_data["profile"].get("id", ""),
                "outreach_variants": [],
                "talking_points": [],
                "recommended_channel": "email",
                "follow_up_timing": "Placeholder — implement LLM call",
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
            and "critic_result" in input_data
            and input_data.get("critic_result", {}).get("verdict") == "approved"
        )

    def validate_output(self, result: AgentResult) -> bool:
        if result.status != "success":
            return False
        data = result.data
        required = {"offer_id", "profile_id", "outreach_variants", "recommended_channel"}
        return required.issubset(data.keys())

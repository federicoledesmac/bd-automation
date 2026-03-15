"""
Gap Finder Agent — Auxiliary Agent
====================================
Purpose: Identifies missing or incomplete data in profiles, offers, and empathy
maps that would improve matching quality. Runs independently from the main pipeline.

Model strategy: Cheap/fast model for structured analysis (e.g., mistral-small)

Use cases:
  - Pre-pipeline: flag incomplete profiles before they enter matching
  - Post-pipeline: identify what data gaps caused low scores
  - Periodic: audit data quality across the entire dataset

Feeds back into ingestion layer to prioritize data collection.
"""

from __future__ import annotations

from typing import Any

from agents.base import AgentConfig, AgentResult, BaseAgent

DEFAULT_CONFIG = AgentConfig(
    name="gap_finder",
    model="mistralai/mistral-small-latest",
    temperature=0.1,
    max_tokens=2048,
    max_retries=1,
    prompt_template="gap_finder_agent.md",
    timeout_seconds=30,
)

# Fields expected per entity type for completeness checks
EXPECTED_FIELDS = {
    "offer": [
        "title", "services", "verticals", "tech_stack", "pricing_model",
        "case_studies", "team_capabilities", "delivery_timeline",
    ],
    "profile": [
        "company", "industry", "sub_industry", "company_size", "tech_used",
        "funding_stage", "decision_makers", "pain_points", "budget_range",
    ],
    "empathy_map": [
        "thinks", "feels", "says", "does", "pain_points", "gains",
        "goals", "influences", "preferred_channels",
    ],
}


class GapFinderAgent(BaseAgent):
    """Identifies missing data that would improve matching quality."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        super().__init__(config or DEFAULT_CONFIG)

    async def run(self, input_data: dict[str, Any]) -> AgentResult:
        """
        Analyze entities for data completeness and quality gaps.

        Input schema:
            {
                "entity_type": "offer" | "profile" | "empathy_map",
                "entity": { ... },
                "context": {
                    "low_score_dimensions": [str] | null,
                    "pipeline_stage": str | null
                }
            }

        Output schema:
            {
                "entity_type": str,
                "entity_id": str,
                "completeness_score": float (0-1),
                "missing_fields": [
                    {
                        "field": str,
                        "importance": "critical" | "high" | "medium" | "low",
                        "impact": str,
                        "suggested_source": str | null
                    }
                ],
                "quality_issues": [
                    {
                        "field": str,
                        "issue": "vague" | "outdated" | "inconsistent" | "too_short",
                        "current_value_summary": str,
                        "suggestion": str
                    }
                ],
                "recommended_actions": [str],
                "priority": "critical" | "high" | "medium" | "low"
            }
        """
        if not self.validate_input(input_data):
            return AgentResult(
                agent_name=self.config.name,
                status="error",
                errors=["Invalid input: missing entity_type or entity"],
            )

        entity_type = input_data["entity_type"]
        entity = input_data["entity"]
        expected = EXPECTED_FIELDS.get(entity_type, [])

        # Rule-based completeness check (augmented by LLM for quality)
        missing = [f for f in expected if not entity.get(f)]
        completeness = 1.0 - (len(missing) / max(len(expected), 1))

        prompt = self.load_prompt()

        # TODO: Replace with actual OpenRouter API call for quality analysis
        self.logger.info(
            "Gap analysis: type=%s id=%s completeness=%.1f%%",
            entity_type,
            entity.get("id", "unknown"),
            completeness * 100,
        )

        result = AgentResult(
            agent_name=self.config.name,
            status="success",
            data={
                "entity_type": entity_type,
                "entity_id": entity.get("id", ""),
                "completeness_score": round(completeness, 2),
                "missing_fields": [
                    {
                        "field": f,
                        "importance": "high",
                        "impact": f"Missing {f} reduces matching accuracy",
                        "suggested_source": None,
                    }
                    for f in missing
                ],
                "quality_issues": [],  # Placeholder — LLM will populate
                "recommended_actions": [],
                "priority": "critical" if completeness < 0.5 else
                           "high" if completeness < 0.7 else
                           "medium" if completeness < 0.9 else "low",
            },
            metadata={"model": self.config.model, "expected_fields": expected},
        )

        if not self.validate_output(result):
            result.status = "error"
            result.errors.append("Output validation failed")

        return result

    def validate_input(self, input_data: dict[str, Any]) -> bool:
        return (
            isinstance(input_data, dict)
            and "entity_type" in input_data
            and input_data["entity_type"] in EXPECTED_FIELDS
            and "entity" in input_data
            and isinstance(input_data["entity"], dict)
        )

    def validate_output(self, result: AgentResult) -> bool:
        if result.status != "success":
            return False
        data = result.data
        required = {
            "entity_type", "entity_id", "completeness_score",
            "missing_fields", "quality_issues", "priority",
        }
        return required.issubset(data.keys())

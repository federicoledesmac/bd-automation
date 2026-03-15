"""
BD Automation — Agent Orchestrator
===================================
4-agent sequential pipeline with checkpoints:
  Filter → Score → Critic → Writer

Additional agents:
  - GapFinder: identifies missing data in profiles/offers
  - FeedbackLoop: processes sales team feedback to improve scoring

Architecture: OpenRouter as unified LLM gateway, per-agent model routing.
"""

from agents.filter_agent import FilterAgent
from agents.score_agent import ScoreAgent
from agents.critic_agent import CriticAgent
from agents.writer_agent import WriterAgent
from agents.gap_finder_agent import GapFinderAgent
from agents.feedback_loop_agent import FeedbackLoopAgent

PIPELINE_STAGES = [
    ("filter", FilterAgent),
    ("score", ScoreAgent),
    ("critic", CriticAgent),
    ("writer", WriterAgent),
]

AUXILIARY_AGENTS = {
    "gap_finder": GapFinderAgent,
    "feedback_loop": FeedbackLoopAgent,
}

__all__ = [
    "FilterAgent",
    "ScoreAgent",
    "CriticAgent",
    "WriterAgent",
    "GapFinderAgent",
    "FeedbackLoopAgent",
    "PIPELINE_STAGES",
    "AUXILIARY_AGENTS",
]

"""Lightweight LLM-based summarization.

Uses a small transformers model (CPU) to produce short textual reports
from computed statistics. Keeps latency and memory modest.
"""

from typing import Dict


def summarize(stats: Dict) -> str:
    """Create a concise textual summary from computed metrics.

    Args:
        stats: Dictionary returned by compute_basic_stats.

    Returns:
        A short human-readable paragraph. Placeholder for now.
    """
    return "Summary pending. Stats computed."

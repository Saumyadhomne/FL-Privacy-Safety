"""Minimal federated averaging helper for numeric model weights."""
from __future__ import annotations

from collections.abc import Sequence


def federated_average(client_weights: Sequence[Sequence[float]], sample_counts: Sequence[int] | None = None) -> list[float]:
    """Return a sample-weighted average of client weight vectors."""
    if not client_weights:
        raise ValueError("At least one client update is required")
    width = len(client_weights[0])
    if any(len(weights) != width for weights in client_weights):
        raise ValueError("All client updates must have the same width")
    counts = list(sample_counts or [1] * len(client_weights))
    if len(counts) != len(client_weights) or any(count <= 0 for count in counts):
        raise ValueError("Provide one positive sample count per client")
    total = sum(counts)
    return [sum(weights[i] * count for weights, count in zip(client_weights, counts)) / total for i in range(width)]

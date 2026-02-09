"""Rotated planar surface-code circuit helpers."""
from __future__ import annotations

import stim


def build_rotated_planar_circuit(distance: int, rounds: int) -> stim.Circuit:
    """Build a rotated planar surface-code memory circuit.

    Args:
        distance: Code distance (>1).
        rounds: Number of syndrome measurement rounds (>0).

    Returns:
        Stim circuit implementing the rotated surface-code memory experiment.
    """
    if distance < 2:
        raise ValueError("distance must be >= 2")
    if rounds < 1:
        raise ValueError("rounds must be >= 1")

    return stim.Circuit.generated(
        "surface_code:rotated_memory_x",
        distance=distance,
        rounds=rounds,
    )

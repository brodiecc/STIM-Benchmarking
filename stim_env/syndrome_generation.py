"""Deterministic syndrome dataset generation for decoder benchmarking."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import stim


@dataclass
class SyndromeDataset:
    metadata: dict[str, Any]
    detectors: list[list[int]]
    observables: list[list[int]]

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "metadata": self.metadata,
            "detectors": self.detectors,
            "observables": self.observables,
        }


def generate_syndrome_dataset(
    *,
    distance: int,
    rounds: int,
    shots: int,
    seed: int,
    basis: str = "x",
    after_clifford_depolarization: float = 0.001,
    after_reset_flip_probability: float = 0.0,
    before_measure_flip_probability: float = 0.0,
    before_round_data_depolarization: float = 0.0,
) -> SyndromeDataset:
    """Generate a reproducible rotated surface-code syndrome dataset."""
    if basis not in {"x", "z"}:
        raise ValueError("basis must be 'x' or 'z'")
    if distance < 3 or distance % 2 == 0:
        raise ValueError("distance must be an odd integer >= 3")
    if rounds < 1:
        raise ValueError("rounds must be >= 1")
    if shots < 1:
        raise ValueError("shots must be >= 1")

    task = f"surface_code:rotated_memory_{basis}"
    circuit = stim.Circuit.generated(
        task,
        distance=distance,
        rounds=rounds,
        after_clifford_depolarization=after_clifford_depolarization,
        after_reset_flip_probability=after_reset_flip_probability,
        before_measure_flip_probability=before_measure_flip_probability,
        before_round_data_depolarization=before_round_data_depolarization,
    )
    sampler = circuit.compile_detector_sampler(seed=seed)
    detector_data, observable_data = sampler.sample(
        shots=shots,
        separate_observables=True,
    )

    return SyndromeDataset(
        metadata={
            "task": task,
            "distance": distance,
            "rounds": rounds,
            "shots": shots,
            "seed": seed,
            "noise": {
                "after_clifford_depolarization": after_clifford_depolarization,
                "after_reset_flip_probability": after_reset_flip_probability,
                "before_measure_flip_probability": before_measure_flip_probability,
                "before_round_data_depolarization": before_round_data_depolarization,
            },
            "num_detectors": circuit.num_detectors,
            "num_observables": circuit.num_observables,
        },
        detectors=detector_data.astype("uint8").tolist(),
        observables=observable_data.astype("uint8").tolist(),
    )

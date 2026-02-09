#!/usr/bin/env python3
"""CLI for generating reproducible Stim syndrome datasets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from stim_env.syndrome_generation import generate_syndrome_dataset


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--distance", type=int, required=True)
    parser.add_argument("--rounds", type=int, required=True)
    parser.add_argument("--shots", type=int, required=True)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--basis", choices=["x", "z"], default="x")
    parser.add_argument("--after-clifford-depolarization", type=float, default=0.001)
    parser.add_argument("--after-reset-flip-probability", type=float, default=0.0)
    parser.add_argument("--before-measure-flip-probability", type=float, default=0.0)
    parser.add_argument("--before-round-data-depolarization", type=float, default=0.0)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    dataset = generate_syndrome_dataset(
        distance=args.distance,
        rounds=args.rounds,
        shots=args.shots,
        seed=args.seed,
        basis=args.basis,
        after_clifford_depolarization=args.after_clifford_depolarization,
        after_reset_flip_probability=args.after_reset_flip_probability,
        before_measure_flip_probability=args.before_measure_flip_probability,
        before_round_data_depolarization=args.before_round_data_depolarization,
    )
    args.output.write_text(json.dumps(dataset.to_json_dict(), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Generate syndrome samples for a rotated planar surface code."""
from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import stim

from stim_env.rotated_planar import build_rotated_planar_circuit


@dataclass
class Metadata:
    distance: int
    rounds: int
    shots: int
    num_detectors: int
    num_observables: int


def _bitstring(bits) -> str:
    return "".join("1" if bit else "0" for bit in bits)


def _write_json(path: Path, detectors, observables, metadata: Metadata) -> None:
    payload = {
        "metadata": asdict(metadata),
        "detectors": detectors,
        "observables": observables,
    }
    path.write_text(json.dumps(payload, indent=2))


def _write_csv(path: Path, detectors, observables, metadata: Metadata) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "distance",
                "rounds",
                "shot",
                "detectors",
                "observables",
            ],
        )
        writer.writeheader()
        for shot_index, (det, obs) in enumerate(zip(detectors, observables)):
            writer.writerow(
                {
                    "distance": metadata.distance,
                    "rounds": metadata.rounds,
                    "shot": shot_index,
                    "detectors": _bitstring(det),
                    "observables": _bitstring(obs),
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--distance", type=int, required=True)
    parser.add_argument("--rounds", type=int, required=True)
    parser.add_argument("--shots", type=int, default=10)
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("syndrome.json"),
        help="Output file path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    circuit = build_rotated_planar_circuit(args.distance, args.rounds)
    sampler = circuit.compile_detector_sampler()
    detectors, observables = sampler.sample(
        args.shots, separate_observables=True
    )

    metadata = Metadata(
        distance=args.distance,
        rounds=args.rounds,
        shots=args.shots,
        num_detectors=circuit.num_detectors,
        num_observables=circuit.num_observables,
    )

    if args.format == "json":
        _write_json(args.output, detectors.tolist(), observables.tolist(), metadata)
    else:
        _write_csv(args.output, detectors, observables, metadata)


if __name__ == "__main__":
    main()

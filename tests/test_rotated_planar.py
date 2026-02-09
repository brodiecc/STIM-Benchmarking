import stim

from stim_env.rotated_planar import build_rotated_planar_circuit


def test_rotated_planar_detector_shapes():
    circuit = build_rotated_planar_circuit(distance=3, rounds=2)
    sampler = circuit.compile_detector_sampler()

    shots = 4
    detectors, observables = sampler.sample(shots, separate_observables=True)

    assert isinstance(circuit, stim.Circuit)
    assert detectors.shape == (shots, circuit.num_detectors)
    assert observables.shape == (shots, circuit.num_observables)

# STIM Benchmarking

Step-by-step rebuild for generating controlled syndrome datasets and benchmarking decoders.

## Step 1: Reproducible syndrome generation

Generate a rotated surface-code memory experiment with fixed noise parameters and RNG seed:

```bash
python scripts/generate_syndromes.py \
  --distance 3 \
  --rounds 3 \
  --shots 100 \
  --seed 12345 \
  --basis x \
  --after-clifford-depolarization 0.001 \
  --output syndromes.json
```

Output JSON schema:
- `metadata`: experiment settings and circuit shape.
- `detectors`: detector events per shot (`0/1` values).
- `observables`: logical observable flips per shot (`0/1` values).

Use the same `syndromes.json` input when comparing multiple decoders to keep evaluation controlled.

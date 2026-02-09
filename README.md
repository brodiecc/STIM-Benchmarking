# STIM Benchmarking Utilities

## Syndrome generation

This repository includes a minimal helper for building rotated planar surface-code
circuits with Stim and sampling syndrome data.

### Example

```bash
python scripts/generate_syndrome.py --distance 3 --rounds 2 --shots 5 --format json --output syndromes.json
```

The JSON output includes `metadata`, `detectors`, and `observables` arrays.

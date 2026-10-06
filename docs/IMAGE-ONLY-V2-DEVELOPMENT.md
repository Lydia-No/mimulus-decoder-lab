# Image-only v2 — development boundary

Status: development implementation. Historical use is not authorized.

`image-only-001.0` failed the prospective image calibration gate and is blocked from further substantive historical reuse.

Version 2 addresses the observed failure mode without using f113r as a tuning target. The design requirement is to distinguish macro organization from generic periodic texture.

Three decoder families are retained, but all receive new blind codes and representations:

- **A3 — macro horizontal-run bands.** Counts only dark horizontal runs above a fixed minimum width before testing vertical band regularity. Fine periodic texture made of narrow marks should therefore not qualify merely because it is periodic.
- **B6 — smoothed gradient periodicity plus spatial concentration.** Requires periodicity to survive Gaussian smoothing, requires nontrivial macro gradient amplitude in the central field, rejects lower-bound central lags, and requires repeated margin energy to be horizontally concentrated rather than spread across the margin crop.
- **C9 — macro connected-component row clustering.** Removes tiny components before constructing repeated row or margin loci, then requires repeated multi-component rows with bounded gap variability.

## Development material

`historical/image_v2_development.py` contains eight synthetic development conditions across independent seeds and geometry variants:

- two positive structured cases;
- two vertically disrupted central-field cases with margin markers retained;
- two margin-ablation cases;
- two fine periodic texture/null cases.

Each case contains two known-answer claims: horizontal macro repetition and discrete left-margin repetition. The development gate is strict: all three decoder families must classify all 16 cells correctly.

These cases are development material, not holdout evidence. They may be inspected while implementing v2.

## Freeze rule

After the development implementation is merged:

1. the decoder file and thresholds are frozen;
2. no f113r output is generated;
3. a new synthetic held-out generator is created in a separate change, with different seeds and geometric parameters not present in the development set;
4. the held-out answer key is fixed before execution;
5. failure on any held-out cell blocks historical use of that decoder version;
6. held-out failure may motivate `image-only-003`, but the held-out set may not be reused as a development set for `image-only-002`.

Only a complete held-out pass can authorize a separately preregistered return to f113r.

No transcription, language model, semantic hypothesis, translation, or Voynich-derived threshold is part of this development process.

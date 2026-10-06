# Image-only v3 — development boundary

Status: development candidate. Historical use is not authorized.

`image-only-002.0-dev` passed its development set but failed the separately frozen held-out gate because B6 used a fixed absolute upper margin-lag bound of 120 px. A3 and C9 each scored 20/20 on that held-out set; B6 scored 17/20, with all three misses occurring on valid margin repetitions at lags 130 or 138 px.

Version 3 therefore keeps A3 and C9 unchanged and replaces only B6 with B7.

## B7 change

B7 retains:

- grayscale image only;
- Gaussian-smoothed gradient periodicity;
- central macro-gradient amplitude requirement;
- margin horizontal concentration requirement.

It changes the periodic scale representation: margin lag is evaluated as a fraction of the margin crop height rather than against a fixed absolute upper pixel ceiling.

This is a new decoder version. The failed v2 held-out set is now development evidence and is explicitly disqualified from serving as validation for v3.

## Development set

The v3 development matrix contains:

- all ten former v2 held-out conditions, now treated as inspected development material;
- three additional marker-only scale sweeps;
- two structured scale sweeps;
- one additional periodic-texture null.

The pass criterion is strict: A3, B7, and C9 must classify every development cell correctly.

## Freeze and validation rule

If development passes, the candidate decoder file is frozen before any v3 holdout is created. A fresh v3 holdout must use new seeds and geometry not present in either the original development set, the v2 holdout, or the v3 development additions.

Any v3 held-out miss blocks historical use and requires another version. A v3 holdout result may not be repaired inside the same candidate version.

No f113r input, transcription, semantic hypothesis, translation, or Voynich-derived threshold is part of v3 development.

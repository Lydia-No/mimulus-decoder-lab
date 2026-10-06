# Image-only v3 development 001

Status: PASS on development material only.

Frozen decoder blob: `24cd6a61c1744657ef6bbd62b14ee47a0afb8c8d`

Workflow run: `37399090524`
Artifact: `11384197804`
Artifact ZIP SHA-256: `46aceeedb67ab7cd46534fe1634cb8622bd7b97e99d1c42b217050728113a1f9`

## Result

- A3: 32 / 32
- B7: 32 / 32
- C9: 32 / 32
- Total: 96 / 96 decoder-condition cells

B7 correctly handled all three former B6 scale misses after replacing the fixed absolute upper lag bound with a relative-scale representation. It also retained rejection of periodic texture and sparse nulls.

This is development evidence only. The former v2 held-out set is now part of the inspected development history and cannot validate v3.

The decoder blob above is frozen before creation of a new v3 held-out set. Historical f113r use remains unauthorized until that fresh holdout passes prospectively.

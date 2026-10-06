# Image-only v2 development 001

Status: PASS on development material only.

Frozen decoder blob: `75207864d07573edf53fe29b321381e732347b91`

Workflow run: `37398461965`
Artifact: `11384327892`
Artifact ZIP SHA-256: `f51650cc938e2a26745a4529fda9dbe82e340bb8065741bcdb21c4eea628d167`

## Result

- A3: 16 / 16
- B6: 16 / 16
- C9: 16 / 16
- Total: 48 / 48 decoder-condition cells

The development set varied seed, line spacing, marker spacing, central disruption density, and periodic texture geometry. The specific v1 false-positive mode on fine periodic texture was absent across both development nulls.

## What this establishes

Only that the v2 implementation can distinguish the declared synthetic development conditions under the fixed rules in `historical/image_decoders_v2.py`.

It does not establish transportability to historical material, correctness on f113r, linguistic structure, translation, or decipherment.

## Freeze

The decoder blob identified above is now the candidate subjected to held-out evaluation. It must not be modified after the held-out generator or outputs are inspected.

The held-out set must use different seeds and geometric parameters and must be added prospectively in a separate change. Any held-out failure blocks historical use of this v2 candidate and motivates a new decoder version rather than retuning this one against the held-out cases.

#!/usr/bin/env python3
import json, os, sys
import image_decoders_v3 as D
import image_v2_holdout as OLD

KEYS=["horizontal-repetition","left-margin-discrete-repetition"]

EXTRA={
  "marker_scale_low":{"kind":"marker_only","seed":52001,"marker_spacing":145,"expected":["not_detected","present"]},
  "marker_scale_mid":{"kind":"marker_only","seed":52002,"marker_spacing":220,"expected":["not_detected","present"]},
  "marker_scale_high":{"kind":"marker_only","seed":52003,"marker_spacing":245,"expected":["not_detected","present"]},
  "structured_scale_low":{"kind":"structured","seed":52004,"line_spacing":66,"marker_spacing":145,"jitter":2,"margin":True,"expected":["present","present"]},
  "structured_scale_high":{"kind":"structured","seed":52005,"line_spacing":66,"marker_spacing":245,"jitter":2,"margin":True,"expected":["present","present"]},
  "texture_wide_null":{"kind":"texture","seed":52006,"vspacing":92,"xspacing":53,"barw":7,"barh":18,"expected":["not_detected","not_detected"]}
}


def make_extra(cfg):
    if cfg["kind"]=="marker_only": return OLD.marker_only(cfg)
    if cfg["kind"]=="structured": return OLD.structured(cfg)
    if cfg["kind"]=="texture": return OLD.texture(cfg)
    raise ValueError(cfg["kind"])


def evaluate_case(result,name,image,expected_list):
    expected=dict(zip(KEYS,expected_list)); result["cases"][name]={"expected":expected,"decoders":{}}
    for run in D.run_all(image,name,None):
        code=run["decoder"]["blindCode"]; actual=D.claims_map(run)
        cells={k:{"expected":expected[k],"actual":actual[k],"correct":actual[k]==expected[k]} for k in KEYS}
        result["cases"][name]["decoders"][code]={"measurements":run["measurements"],"cells":cells}


def main():
    if len(sys.argv)!=2: raise SystemExit("usage: image_v3_development.py OUTPUT_DIR")
    out=sys.argv[1]; os.makedirs(out,exist_ok=True)
    result={"development_id":"image-only-v3-development-001","decoder_version":D.RUN_VERSION,"cases":{},"scores":{},"gate":{}}

    # The failed v2 held-out set is explicitly development evidence for v3 and is never reused as v3 validation.
    for name,cfg in OLD.HOLDOUT.items():
        evaluate_case(result,"v2heldout_"+name,OLD.make(cfg),cfg["expected"])
    for name,cfg in EXTRA.items():
        evaluate_case(result,name,make_extra(cfg),cfg["expected"])

    for code in ["A3","B7","C9"]:
        cells=[]
        for case in result["cases"].values(): cells.extend(case["decoders"][code]["cells"].values())
        correct=sum(1 for c in cells if c["correct"])
        result["scores"][code]={"correct":correct,"total":len(cells),"passed":correct==len(cells)}
    result["gate"]={"criterion":"all three candidate decoders must classify every v3 development cell correctly","passed":all(v["passed"] for v in result["scores"].values())}
    result["boundary"]="Development only. Includes the former v2 holdout because its outcome has already been inspected. A fresh v3 holdout must be created only after this decoder candidate is frozen."
    with open(os.path.join(out,"development.json"),"w",encoding="utf-8") as f: json.dump(result,f,indent=2,sort_keys=True)
    print(json.dumps(result,indent=2,sort_keys=True))
    if not result["gate"]["passed"]: raise SystemExit(2)

if __name__=="__main__": main()
